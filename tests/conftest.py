import numpy as np
import pytest


T, H, W = 40, 5, 7  # minimal synthetic shape: (time, grid_h, grid_w)


def pytest_addoption(parser):
    parser.addoption(
        '--data-dir',
        action='store',
        default=None,
        metavar='PATH',
        help='Path to real preprocessed fNIRS data directory (e.g. ./data). '
             'Enables real-data variants of leakage tests.',
    )

_GROUPS = {
    'healthy': ['AH01', 'AH02', 'AH03', 'AH04'],
    'anxiety': ['AA01', 'AA02', 'AA03', 'AA04'],
}
_TRIALS_PER_SUBJECT = 2


@pytest.fixture(scope='session')
def synthetic_data_dir(tmp_path_factory):
    """Creates a minimal preprocessed fNIRS directory tree for all tests.

    Structure mirrors processor_cli.py output:
      {root}/{task}/{group}/{subject}/hbt/{trial_idx}.npy
    """
    root = tmp_path_factory.mktemp('fnirs_data')
    for task in ['GNG']:
        for group, subjects in _GROUPS.items():
            for subject in subjects:
                data_dir = root / task / group / subject / 'hbt'
                data_dir.mkdir(parents=True)
                rng = np.random.default_rng(seed=abs(hash(subject)) % (2 ** 32))
                for trial_idx in range(_TRIALS_PER_SUBJECT):
                    arr = rng.standard_normal((T, H, W)).astype(np.float32)
                    np.save(data_dir / f'{trial_idx}.npy', arr)
    return root


@pytest.fixture(scope='session')
def real_data_dir(request):
    """Returns the real data directory path, or None if --data-dir was not supplied."""
    return request.config.getoption('--data-dir')


@pytest.fixture(scope='session', params=['synthetic', 'real'])
def any_data_dir(request, synthetic_data_dir, real_data_dir):
    """Parametrized fixture: runs each test with synthetic data (always) and real data
    (only when --data-dir is supplied; otherwise the real variant is skipped).
    """
    if request.param == 'real':
        if real_data_dir is None:
            pytest.skip('Real-data variant requires --data-dir (e.g. --data-dir ./data)')
        return real_data_dir
    return str(synthetic_data_dir)
