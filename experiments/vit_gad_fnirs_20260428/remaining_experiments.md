# Remaining Experiments

Reference command:
```
python -m core.main --data_dir data/processed/ --batch_size 8 --epochs 100 --use_kfold --k_folds 10 --task GNG --data_type hbo --patience 100 --splits_json data/splits/kfold_splits.json --num_workers 4
```

**Status:** 10 remaining (14 total gap including hbr; GNG is fully complete)

---

## SS (2 remaining)

### hbo-10fold
```bash
python -m core.main --data_dir data/processed/ --batch_size 8 --epochs 100 --use_kfold --k_folds 10 --task SS --data_type hbo --patience 100 --splits_json data/splits/kfold_splits.json --num_workers 4 ✅
```

### hbr-10fold
```bash
python -m core.main --data_dir data/processed/ --batch_size 8 --epochs 100 --use_kfold --k_folds 10 --task SS --data_type hbr --patience 100 --splits_json data/splits/kfold_splits.json --num_workers 4 ✅
```

---

## 1backWM (4 remaining)

### hbo-5fold
```bash
python -m core.main --data_dir data/processed/ --batch_size 8 --epochs 100 --use_kfold --k_folds 5 --task 1backWM --data_type hbo --patience 100 --splits_json data/splits/kfold_splits.json --num_workers 4 ✅
```

### hbo-10fold
```bash
python -m core.main --data_dir data/processed/ --batch_size 8 --epochs 100 --use_kfold --k_folds 10 --task 1backWM --data_type hbo --patience 100 --splits_json data/splits/kfold_splits.json --num_workers 4 ✅
```

### hbr-5fold
```bash
python -m core.main --data_dir data/processed/ --batch_size 8 --epochs 100 --use_kfold --k_folds 5 --task 1backWM --data_type hbr --patience 100 --splits_json data/splits/kfold_splits.json --num_workers 4 ✅
```

### hbr-10fold
```bash
python -m core.main --data_dir data/processed/ --batch_size 8 --epochs 100 --use_kfold --k_folds 10 --task 1backWM --data_type hbr --patience 100 --splits_json data/splits/kfold_splits.json --num_workers 4 ✅
```

---

## VF (4 remaining)

### hbo-5fold
```bash
python -m core.main --data_dir data/processed/ --batch_size 8 --epochs 100 --use_kfold --k_folds 5 --task VF --data_type hbo --patience 100 --splits_json data/splits/kfold_splits.json --num_workers 4 ✅
```

### hbo-10fold
```bash
python -m core.main --data_dir data/processed/ --batch_size 8 --epochs 100 --use_kfold --k_folds 10 --task VF --data_type hbo --patience 100 --splits_json data/splits/kfold_splits.json --num_workers 4 ✅
```

### hbr-5fold
```bash
python -m core.main --data_dir data/processed/ --batch_size 8 --epochs 100 --use_kfold --k_folds 5 --task VF --data_type hbr --patience 100 --splits_json data/splits/kfold_splits.json --num_workers 4 ✅
```

### hbr-10fold
```bash
python -m core.main --data_dir data/processed/ --batch_size 8 --epochs 100 --use_kfold --k_folds 10 --task VF --data_type hbr --patience 100 --splits_json data/splits/kfold_splits.json --num_workers 4 ✅
```
