import pandas as py
import numpy as np
import mne


def text_to_raw(file,location):
    eeg_df = pd.read_table(file,header = None)
    locs_df = pd.read_table(location,header = None)
