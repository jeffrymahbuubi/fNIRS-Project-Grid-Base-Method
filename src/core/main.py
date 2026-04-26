import yaml
from argparse import ArgumentParser
import os
from datetime import date
import torch
from torch import optim
from torchvision.transforms.v2 import Compose, UniformTemporalSubsample, Resize

from .config import SystemConfig, setup_system
from .models import ViT
from .training import main as training_main, CosineWarmupScheduler
from .datasets import RearrangeToTCHW, RearrangeBackToCTHW, ConvertToRGB, AddGaussianNoise


def build_parser() -> ArgumentParser:
    parser = ArgumentParser(
        description="fNIRS Anxiety Project: Multi-GPU Training"
    )
    parser.add_argument(
        '--data_dir',
        type=str,
        default='./data',
        help="Path to data directory"
    )
    parser.add_argument(
        '--save_dir',
        type=str,
        default='./experiments/saved_models',
        help="Base directory for new experiments. When --resume is set, must be the full path to the existing experiment directory."
    )
    parser.add_argument(
        '--batch_size',
        type=int,
        default=8,
        help="Batch size for training"
    )
    parser.add_argument(
        '--epochs',
        type=int,
        default=100,
        help="Number of epochs"
    )
    parser.add_argument(
        '--use_kfold',
        action='store_true',
        help="Use k-fold cross validation"
    )
    parser.add_argument(
        '--k_folds',
        type=int,
        default=5,
        help="Number of folds for k-fold cross validation (if selected)"
    )
    parser.add_argument(
        '--use_loso',
        action='store_true',
        help="Use leave-one-subject-out cross validation"
    )
    parser.add_argument(
        '--task',
        type=str,
        default='GNG',
        choices=['GNG', '1backWM', 'VF', 'SS'],
        help="Task to train: GNG, 1backWM, VF, or SS"
    )
    parser.add_argument(
        '--data_type',
        type=str,
        default='hbt',
        choices=['hbt', 'hbo', 'hbr', 'all'],
        help="Hemoglobin concentration type: hbt (total), hbo (oxy), hbr (deoxy), all"
    )
    parser.add_argument(
        '--use_class_weights',
        action='store_true',
        help="Enable class weighting via CrossEntropyLoss (default: off)"
    )
    parser.add_argument(
        '--sqrt_class_weights',
        action='store_true',
        help="Apply sqrt softening to class weights (only used if --use_class_weights is set)"
    )
    parser.add_argument(
        '--patience',
        type=int,
        default=25,
        help="Early stopping patience in epochs (default: 25)"
    )
    parser.add_argument(
        '--use_amp',
        action='store_true',
        help="Enable bfloat16 Automatic Mixed Precision (default: off)"
    )
    parser.add_argument(
        '--label_smoothing',
        type=float,
        default=0.0,
        help="Label smoothing epsilon for CrossEntropyLoss, e.g. 0.1 (default: 0.0, off)"
    )
    parser.add_argument(
        '--splits_json',
        type=str,
        default=None,
        help="Path to predefined k-fold splits JSON (required when --use_kfold is set)"
    )
    parser.add_argument(
        '--resume',
        action='store_true',
        help="Resume training — skip folds/subjects already trained. Requires --save_dir to point to the existing experiment directory."
    )
    parser.add_argument(
        '--num_workers',
        type=int,
        default=1,
        help="Number of DataLoader worker processes (default: 1)"
    )
    return parser


def build_experiment_name(args, model_name: str) -> str:
    if args.use_loso:
        cv = "loso"
    elif args.use_kfold:
        cv = f"kfold{args.k_folds}"
    else:
        cv = "holdout"
    if args.use_class_weights and args.sqrt_class_weights:
        cw = "_cwsqrt"
    elif args.use_class_weights:
        cw = "_cw"
    else:
        cw = ""
    amp = "_amp" if args.use_amp else ""
    ls = f"_ls{int(args.label_smoothing * 100)}" if args.label_smoothing > 0 else ""
    today = date.today().strftime("%Y%m%d")
    return f"{model_name}_{args.task}_{args.data_type}_{cv}{cw}{amp}{ls}_ep{args.epochs}_bs{args.batch_size}_p{args.patience}_{today}"


def main():
    import sys

    # Pass 1: extract --resume and --save_dir to locate saved config
    pre_parser = ArgumentParser(add_help=False)
    pre_parser.add_argument('--resume', action='store_true')
    pre_parser.add_argument('--save_dir', type=str, default='./experiments/saved_models')
    pre_args, _ = pre_parser.parse_known_args()

    # Load saved config when resuming so all original args are restored
    saved_defaults = {}
    if pre_args.resume:
        config_path = os.path.join(pre_args.save_dir, 'config.yaml')
        if os.path.exists(config_path):
            with open(config_path) as f:
                saved_defaults = yaml.safe_load(f) or {}
            print(f"Loaded config from: {config_path}")

    # Pass 2: full parse — saved config slots in as defaults, CLI args override
    parser = build_parser()
    if saved_defaults:
        parser.set_defaults(**saved_defaults)
    args = parser.parse_args()

    if args.use_kfold and not args.splits_json:
        print("error: --splits_json is required when --use_kfold is set.\n"
              "Generate it once with: python data/generate_splits.py --processed_dir <dir>",
              file=sys.stderr)
        sys.exit(2)

    if args.resume and not (args.use_loso or args.use_kfold):
        print("error: --resume is only valid with --use_loso or --use_kfold", file=sys.stderr)
        sys.exit(2)

    if args.resume and not os.path.isdir(args.save_dir):
        print(f"error: --resume requires --save_dir to be an existing experiment directory.\n"
              f"  '{args.save_dir}' does not exist.\n"
              f"  Pass the full path to the original experiment folder, e.g.:\n"
              f"  --save_dir experiments/saved_models/ViT_GNG_hbt_loso_cwsqrt_ep200_bs8_p100_20260422",
              file=sys.stderr)
        sys.exit(2)

    setup_system(SystemConfig)

    num_classes = 2
    image_size = (128, 128)
    image_patch_size = (8, 8)
    frames = 256
    frame_patch_size = 16
    channels = 3
    dim = 64
    depth = 6
    heads = 8
    mlp_dim = 512

    model = ViT(
        image_size=image_size,
        image_patch_size=image_patch_size,
        frames=frames,
        frame_patch_size=frame_patch_size,
        num_classes=num_classes,
        dim=dim,
        depth=depth,
        heads=heads,
        mlp_dim=mlp_dim,
        channels=channels
    )

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    train_transform = Compose([
        RearrangeToTCHW(),
        UniformTemporalSubsample(num_samples=256),
        Resize((128, 128)),
        RearrangeBackToCTHW(),
        ConvertToRGB(),
        AddGaussianNoise(mean=0.0, std=0.05)
    ])

    val_transform = Compose([
        RearrangeToTCHW(),
        UniformTemporalSubsample(num_samples=256),
        Resize((128, 128)),
        RearrangeBackToCTHW(),
        ConvertToRGB()
    ])

    optimizer = optim.Adam(model.parameters(), lr=1e-3)
    scheduler = CosineWarmupScheduler(optimizer, warmup=10, max_iters=args.epochs)

    task_name = args.task
    data_type = args.data_type
    test_size = 0.2
    model_name = 'ViT'

    if args.resume:
        exp_dir = args.save_dir
        print(f"Resuming experiment: {exp_dir}")
        config_out = os.path.join(exp_dir, 'config.yaml')
        if not os.path.exists(config_out):
            with open(config_out, 'w') as f:
                yaml.dump(vars(args), f, default_flow_style=False, sort_keys=True)
            print(f"Config backfilled: {config_out}")
    else:
        exp_name = build_experiment_name(args, model_name)
        exp_dir = os.path.join(args.save_dir, exp_name)
        print(f"Experiment dir: {exp_dir}")
        os.makedirs(exp_dir, exist_ok=True)
        config_out = os.path.join(exp_dir, 'config.yaml')
        with open(config_out, 'w') as f:
            yaml.dump(vars(args), f, default_flow_style=False, sort_keys=True)
        print(f"Config saved: {config_out}")

    training_main(
        data_dir=args.data_dir,
        save_dir=exp_dir,
        test_size=test_size,
        data_type=data_type,
        model=model,
        model_name=model_name,
        task_name=task_name,
        optimizer=optimizer.__class__,
        optimizer_params={"lr": 1e-3},
        scheduler=scheduler.__class__,
        scheduler_params={"warmup": 10, "max_iters": args.epochs},
        batch_size=args.batch_size,
        epochs_count=args.epochs,
        device='cuda',
        use_amp=args.use_amp,
        use_kfold=args.use_kfold,
        k_folds=args.k_folds,
        use_loso=args.use_loso,
        use_class_weights=args.use_class_weights,
        use_sqrt_class_weights=args.sqrt_class_weights,
        max_trials=4,
        train_transform=train_transform,
        val_transform=val_transform,
        patience=args.patience,
        label_smoothing=args.label_smoothing,
        splits_json=args.splits_json,
        resume=args.resume,
        num_workers=args.num_workers
    )


if __name__ == '__main__':
    main()
