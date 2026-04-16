from argparse import ArgumentParser
import torch
from torch import nn, optim
from torchvision.transforms.v2 import Compose, UniformTemporalSubsample, Resize

from .config import TrainingConfiguration, SystemConfig, setup_system
from .models import ViT
from .training import main as training_main, CosineWarmupScheduler, LabelSmoothing
from .datasets import RearrangeToTCHW, RearrangeBackToCTHW, ConvertToRGB, AddGaussianNoise


def parse_args():
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
        help="Directory to save models"
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
    return parser.parse_args()


def main():
    args = parse_args()

    train_config = TrainingConfiguration(
        batch_size=args.batch_size,
        epochs_count=args.epochs,
        device='cuda'
    )
    setup_system(SystemConfig)

    num_classes = 1
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
    loss_fn = LabelSmoothing(smoothing=0.1)

    # Use the task argument to set up the task configuration
    task_types = {args.task: {'window_duration': 1}}
    data_type = 'hbt'
    test_size = 0.2
    model_name = 'ViT'

    training_main(
        data_dir=args.data_dir,
        save_dir=args.save_dir,
        test_size=test_size,
        data_type=data_type,
        model=model,
        model_name=model_name,
        task_types=task_types,
        optimizer=optimizer.__class__,
        optimizer_params={"lr": 1e-3},
        scheduler=scheduler.__class__,
        scheduler_params={"warmup": 10, "max_iters": args.epochs},
        training_configuration=train_config,
        use_kfold=args.use_kfold,
        k_folds=args.k_folds,
        use_loso=args.use_loso,
        loss_fn=loss_fn,
        max_trials=4,
        train_transform=train_transform,
        val_transform=val_transform
    )


if __name__ == '__main__':
    main()
