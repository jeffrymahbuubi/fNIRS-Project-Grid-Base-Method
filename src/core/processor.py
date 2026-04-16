import mne
from mne import create_info
import pandas as pd
import numpy as np
import copy
from pathlib import Path


class FNIRSDataProcessor:
    """
    Process fNIRS data for specific subjects, groups, and tasks.

    Parameters:
    - root_dir: Path to directory containing 'healthy' and 'anxiety' folders
    - subject: Subject identifier (string)
    - group: 'healthy' or 'anxiety'
    - task_type: 'GNG', '1backWM', 'VF', or 'SS'
    - data_type: 'hbo', 'hbr', or 'hbt'
    - apply_baseline: bool, whether to apply baseline correction
    - apply_zscore: bool, whether to apply z-score normalization
    - save_preprocessed: bool, whether to save each epoch as .npy and .csv
    - montage_file: path to custom montage file (optional)
    - ppf: partial pathlength factor for Beer-Lambert law
    """
    def __init__(
        self,
        root_dir,
        subject,
        group,
        task_type='GNG',
        data_type='hbo',
        apply_baseline=False,
        apply_zscore=False,
        save_preprocessed=False,
        montage_file=None,
        ppf=6.0
    ):
        self.root_dir = Path(root_dir)
        self.subject = subject
        self.group = group
        self.task_type = task_type
        self.data_type = data_type.lower()
        self.apply_baseline = apply_baseline
        self.apply_zscore = apply_zscore
        self.save_preprocessed = save_preprocessed
        self.montage_file = montage_file
        self.ppf = ppf

        # Define subject directory: root_dir / group / subject / task
        self.subject_dir = self.root_dir / self.group / self.subject / self.task_type

        # Placeholders
        self.raw_haemo = None
        self.preprocessed = None
        self.epoch_data = None

    def load_data(self):
        """
        Load raw NIRx data, apply OD and Beer-Lambert, and combine HbO/HbR CSVs.
        """
        # Read raw data
        raw = mne.io.read_raw_nirx(self.subject_dir, preload=True, verbose=False)
        # Set custom montage if provided
        if self.montage_file:
            montage = mne.channels.read_custom_montage(self.montage_file, head_size=0.0825)
            raw.set_montage(montage)

        # Convert to optical density and hemoglobin concentration
        raw_od = mne.preprocessing.nirs.optical_density(raw, verbose=False)
        raw_haemo = mne.preprocessing.nirs.beer_lambert_law(raw_od, ppf=self.ppf, verbose=False)

        # Load preprocessed CSV files
        hbo_file = next(self.subject_dir.glob('*HbO.csv'), None)
        hbr_file = next(self.subject_dir.glob('*HbR.csv'), None)
        hbo_df = pd.read_csv(hbo_file, header=None).drop([0, 1]).reset_index(drop=True).astype(float)
        hbr_df = pd.read_csv(hbr_file, header=None).drop([0, 1]).reset_index(drop=True).astype(float)
        assert hbo_df.shape[0] == hbr_df.shape[0], "HbO and HbR rows must match"

        # Interleave rows: HbO, HbR
        combined = pd.DataFrame(np.empty((hbo_df.shape[0] * 2, hbo_df.shape[1])))
        combined.iloc[0::2, :] = hbo_df.values
        combined.iloc[1::2, :] = hbr_df.values

        # Create RawArray and set annotations
        preprocessed = mne.io.RawArray(combined.values, raw_haemo.info)
        preprocessed.set_annotations(raw_haemo.annotations)

        self.raw_haemo = raw_haemo
        self.preprocessed = preprocessed
        return raw_haemo, preprocessed

    def generate_hbt(self):
        """
        Compute HbT channel as HbO + HbR and add to preprocessed data.
        """
        hbo = self.preprocessed.get_data(picks='hbo')
        hbr = self.preprocessed.get_data(picks='hbr')
        hbt = hbo + hbr

        names = [ch.replace('hbo', 'hbt') for ch in self.raw_haemo.ch_names if 'hbo' in ch]
        info = create_info(names, self.preprocessed.info['sfreq'], ch_types='fnirs_cw_amplitude')
        raw_hbt = mne.io.RawArray(hbt, info)
        self.preprocessed.add_channels([raw_hbt])

    def modify_annotations(self):
        """
        Update annotation durations and insert 'Rest' after first baseline.
        """
        ann = copy.deepcopy(self.preprocessed.annotations)
        correct = {'1.0': 120}
        new_on, new_dur, new_desc = [], [], []
        rest_added = False

        for onset, duration, desc in zip(ann.onset, ann.duration, ann.description):
            new_dur.append(correct.get(desc, duration))
            new_on.append(onset)
            new_desc.append(desc)

            if desc == '1.0' and not rest_added:
                new_on.append(onset + correct['1.0'])
                new_dur.append(30)
                new_desc.append('99.0')
                rest_added = True

        updated = mne.Annotations(onset=new_on, duration=new_dur, description=new_desc, orig_time=ann.orig_time)
        self.preprocessed.set_annotations(updated)

    def _baseline_correction(self, epochs):
        """Baseline correct using first Rest epoch (99.0)."""
        rest = epochs['99.0'].get_data()[0]
        idx = np.where((epochs.times >= 0) & (epochs.times <= 5))[0]
        mean = rest[:, idx].mean(axis=1)
        data = epochs.get_data()
        data -= mean[:, np.newaxis]
        epochs._data = data
        return epochs

    def epoch(self):
        """
        Epoch data around events, apply optional baseline and z-score, and save.
        Returns a list of numpy arrays for each epoch.
        """
        durations = {
            'GNG': (0, 35),
            'VF': (0, 60),
            'SS': (0, 60),
            '1backWM': (0, 90)
        }
        tmin, tmax = durations.get(self.task_type, (0, 35))

        # Select picks
        if self.data_type in ['hbo', 'hbr']:
            picks = self.data_type
        else:
            picks = [ch for ch in self.preprocessed.info['ch_names'] if 'hbt' in ch]

        events, event_id = mne.events_from_annotations(self.preprocessed, verbose=False)
        epochs = mne.Epochs(
            self.preprocessed.copy().pick(picks),
            events,
            event_id,
            tmin=tmin,
            tmax=tmax,
            reject_by_annotation=True,
            proj=True,
            baseline=None,
            preload=True,
            detrend=None,
            verbose=False
        )

        if self.apply_baseline:
            epochs = self._baseline_correction(epochs)
        if self.apply_zscore:
            def z(ts): return (ts - ts.mean()) / ts.std()
            epochs.apply_function(z, picks=None, channel_wise=True, verbose=False)

        # Select only task events (3.0) and crop
        if '3.0' in epochs.event_id:
            epochs = epochs['3.0']
        epochs = epochs.crop(tmin=3, tmax=epochs.tmax)

        self.epoch_data = []
        for idx in range(len(epochs)):
            arr = epochs[idx].get_data().squeeze()
            self.epoch_data.append(arr)

            if self.save_preprocessed:
                out_dir = self.subject_dir / self.data_type.upper()
                out_dir.mkdir(parents=True, exist_ok=True)
                np.save(out_dir / f"{idx}.npy", arr)
                pd.DataFrame(arr).to_csv(out_dir / f"{idx}.csv", index=False)

        return self.epoch_data

    def process(self):
        """
        Execute full pipeline: load, optional HbT, annotate, epoch.
        Returns list of epoch arrays.
        """
        self.load_data()
        if self.data_type == 'hbt':
            self.generate_hbt()
        self.modify_annotations()
        return self.epoch()
