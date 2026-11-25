# Signal Lab — EEG Pattern Explorer

An interactive, responsive frontend for exploring EEG signal recordings across interictal, preictal, and ictal stages. It shows actual waveform samples and six numerical features calculated from the complete recordings. This is a research visualization, not a diagnostic device.

## Run locally

```bash
python -m http.server 8000
```

Open `http://localhost:8000`. The frontend is plain HTML, CSS, and JavaScript, with no build step.

## Data preparation

The project was prepared from Danyal's local copy of the **EEG Epilepsy Datasets** collection: 50 interictal, 50 preictal, and 50 ictal CSV recordings. `prepare_data.py` calculates mean, standard deviation, range, RMS power, zero crossing rate, and mean absolute change from every full recording, then saves a downsampled waveform for the browser. Run it against a local copy with:

```bash
python prepare_data.py --source /path/to/CSV
```

The source recordings are not republished here. See the research description [Nonlinear analysis and recognition of epileptic EEG signals in different stages](https://journals.physiology.org/doi/full/10.1152/jn.00055.2024) for context on this 50-recordings-per-stage dataset. The repository contains derived features and display traces, not clinical results. A proper prediction study would require patient independent validation.

An exploratory three-stage classifier can be run with `python train_model.py` after installing scikit-learn. It uses a stratified file-level split and reports a confusion matrix. Its score must not be interpreted as patient-independent or clinical performance.

## Project purpose

This frontend makes EEG pattern exploration more legible for a portfolio audience. The feature extraction script is reproducible, while the interface lets visitors compare recordings and stages directly.
