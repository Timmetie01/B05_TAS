import matplotlib.pyplot as plt
import numpy as np


def test_filter(filtered_data, input_data, difference=False, truth=None, discrete_points=True, showplot=True, filter_shift=0):
    '''
    Graphs the filtered data, input data and if present truth
    
    :param filtered_data: 1 or 2d array of the filtered data. Plotted along axis 1
    :param input_data: 1 or 2d array of the original data points. Plotted along axis 1
    :param difference: Plots the difference between filterd and unfiltered data.
    :param truth: Optional extra 1 or 2d array to be plotted, not implemented quite yet
    :param discrete_points: True represents original data as scatter plot, False gives line represenation
    :param showplot: True styles the plot and calls plt.show(), False doesn't such that another plot can be layered over this one
    :return filter_shift: integer, shifts the input filtered right by that amount of points. Useful when filter shortens the array.
    
    '''
    if truth != None:
        print('plotting a truth is not yet implemented, woops')
        raise NotImplementedError

    if filtered_data.ndim == 1:
        filtered_data = np.transpose(np.array([filtered_data]))
        input_data = np.transpose(np.array([input_data]))
        truth = np.transpose(np.array([truth]))

    if filtered_data.ndim > 2 or input_data.ndim != filtered_data.ndim:
        print('You shouldn\'t input higher than 2 dimensional array, and array dimensions should be the same for filtered and input data.')
        quit()

    for i in range(len(filtered_data[0,:])):
        plt.plot(np.arange(0, len(filtered_data[:,i]), 1) + filter_shift, filtered_data[:,i], label='Filtered data', color='darkblue')
        if discrete_points:
            plt.scatter(np.arange(0, len(input_data[:,i]), 1), input_data[:,i], label='Original data', color='firebrick')
        else:
            plt.plot(np.arange(0, len(input_data[:,i]), 1), input_data[:,i], label='Original data', color='firebrick')
    
        if difference:
            print('Showing the difference is not implemented yet...')
            raise NotImplementedError
        #    filter_delta = input_data[filter_shift:-filter_shift,:] - filtered_data
        #    plt.plot(np.arange(0, len(filtered_data[:,i]), 1) + filter_shift, filter_delta[:,i], label='Difference', color='darkgreen')

    if showplot:
        plt.title('Filtered vs unfiltered data')
        plt.legend()
        plt.show()

    return None

def trajectory_3d_plot(data, target=None, label=None, title=None, showplot=True):
    ax = plt.figure().add_subplot(projection='3d')
    X = data[:,0]
    Y = data[:,1]
    Z = data[:,2]

    ax.plot(X, Y, Z, label=label, color="darkblue")


    if target != None:
        Xt = target[:,0]
        Yt = target[:,1]
        Zt = target[:,2]
        ax.plot(Xt, Yt, Zt, label=f"{label}, target", color="firebrick")

    plt.legend()
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(title)
    if showplot:
        plt.show()