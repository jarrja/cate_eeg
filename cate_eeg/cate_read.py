import pandas as pd
import numpy as np
import mne

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
    
    return raw

if __name__ == '__main__':
    print "CATE_EEG"
