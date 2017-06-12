import pandas as pd
import numpy as np
import mne
import warnings

def text_to_raw(file_name,location,sfreq,col_remove = [],montage_type = 'standard_1020'):
    #Read EEG data from text file
    eeg_df = pd.read_table(file_name,header = None)
    #Read Location from text file
    locs_df = pd.read_table(location,header = None)
    channel_name = [item.strip() for item in locs_df[3].values.tolist()]

    #Remove the desire column
    eeg_df.drop(eeg_df.columns[col_remove],axis = 1, inplace = True)
    #Assign channel name to the dataframe
    eeg_df.columns = channel_name
    eeg_matrix_np = eeg_df.as_matrix().transpose()

    #Create Info MNE File
    channel_type = ['eeg']*19
    info = mne.create_info(ch_names=channel_name,ch_types=channel_type,sfreq = sfreq)

    #Create Raw MNE file
    raw = mne.io.RawArray(eeg_matrix_np,info)

    #Set Montage
    montage = mne.channels.read_montage(montage_type)
    raw.set_montage(montage)
    #Return raw MNE file
    return raw

def edf_to_raw(edf_file_name,chan_select = [],montage_type = 'standard_1020'):
    #If no channel is selcted, assign the default channel to the selection
    if not chan_select:
        warnings.warn('Empty selection of channel, Default channels are selected')
        chan_select = [u'C3', u'C4', u'O1', u'O2', u'Cz', u'F3', u'F4', u'F7', u'F8', u'Fz', u'Fp1', u'Fp2', u'P3', u'P4', u'Pz', u'T3', u'T4', u'T5', u'T6']
    #Read edf file to raw
    raw = mne.io.read_raw_edf(edf_file_name,preload=True)
    #Apply selection of channel
    raw.pick_channels(chan_select)
    #Set montage
    montage = mne.channels.read_montage(montage_type)
    raw.set_montage(montage)
    #Return raw MNE file
    return raw



if __name__ == '__main__':
    print "CATE_EEG"
