import pickle
import numpy as np
import pandas as pd
import os
# Locate mask directory
FUNC_DIR = '/Users/jarr/Dropbox/Research/CATE_EEG_MASTER/cate_eeg'


def connection_count(connectivity_matrix, mask_name, threshold):
    """
    The function count the number of connection within the predefined
    regions (Left Right Hemisphere, Anterior Posterior Axis) under the
    selected threshold.
    :param connectivity_matrix: Connectivity Matrix
    :param mask_name:  Select mask name between 'Baptist' or 'Miami'
    :param threshold: Threshold range from 0.00 to 1.00
    :return: Return connection as lists
    Lists: epoch_connection = [[epoch_1][epoch_2]...[epoch_N]]
    Lists: [epoch_1] = [[freq_1][freq_2]...[freq_N]]
    freq_1 = {'Left': #connection, 'Right': #connection ... 'LRInter':#connection}
    """

    # Select baptist mask for counting
    if mask_name is 'Baptist':
        # Join the pickle directory with the mask name
        pickle_path = os.path.join(FUNC_DIR,'BaptistConnectivityMask.pickle')
        with open(pickle_path, 'rb') as f:
            mask_object = pickle.load(f)
        connectivity_mask = mask_object[0]
    # Select miami mask for counting
    elif mask_name is 'Miami':
        # Join the pickle directory with the mask name
        pickle_path = os.path.join(FUNC_DIR, 'MiamiConnectivityMask.pickle')
        with open(pickle_path, 'rb') as f:
            mask_object = pickle.load(f)
        connectivity_mask = mask_object[0]
    else:
        raise ValueError('Select mask name: Baptist or Miami')

    # Check for the size of frequency
    _, _, freq_size = connectivity_matrix[0].shape
    print 'Number of frequency: {}'.format(freq_size)

    epoch_connection = []
    # Loop through the total length of epochs
    for i in range(len(connectivity_matrix)):
        freq_connection = []
        # Loop through the total frequency bands
        for j in range(freq_size):
            connection = {}
            for index, (key, mask) in enumerate(connectivity_mask.iteritems()):
                connection[key] = (np.multiply(connectivity_matrix[i][:, :, j] +
                                               connectivity_matrix[i][:, :, j].transpose(),
                                               connectivity_mask[key]) >= threshold).sum().sum()
            freq_connection.append(connection)
        epoch_connection.append(freq_connection)

    # Return the count of connection
    return epoch_connection


def connection_to_dataframe(epoch_connection):
    """
    Convert connection from "connection_count" to pandas dataframe
    with alignment
    :param epoch_connection:
    :return: pandas dataframe of connection
    """
    all_con = []
    for i in range(len(epoch_connection)):
        if i < 1:
            for j in range(len(epoch_connection[0])):
                all_con += epoch_connection[i][j].items()
            con_df = pd.DataFrame(all_con, columns=['Region', str(i)])
            all_con = []
        else:
            for j in range(len(epoch_connection[0])):
                all_con += epoch_connection[i][j].values()
            con_df[str(i)] = np.asarray(all_con)
            all_con = []
    return con_df.transpose()


def connection_df_to_excel(df_list, sheets, file_name, spaces):
    """
    Save Connection list of dataframe into excel files. dataframe
    :param df_list: list of dataframe
    :param sheets: Sheets Name
    :param file_name: File Name
    :param spaces: Space between dataframe in excel
    :return: None
    """
    writer = pd.ExcelWriter(file_name,engine='xlsxwriter')
    row = 0
    for dataframe in df_list:
        dataframe.to_excel(writer,sheet_name=sheets,startrow=row , startcol=0)
        row = row + len(dataframe.index) + spaces + 1
    writer.save()


