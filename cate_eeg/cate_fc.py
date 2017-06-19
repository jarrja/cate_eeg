import pickle
import numpy as np


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
        with open('BaptistConnectivityMask.pickle', 'rb') as f:
            mask_object = pickle.load(f)
        connectivity_mask = mask_object[0]
    # Select miami mask for counting
    elif mask_name is 'Miami':
        with open('MiamiConnectivityMask.pickle', 'rb') as f:
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

    # print connectivity_mask.keys()


# with open('objs.pickle','rb') as f:
#     con = pickle.load(f)
#
# print con[0].shape
# epoch_connection = connection_count(con, 'Miami', 0.5)
#
# print len(epoch_connection)
#
# print epoch_connection[0][5]

