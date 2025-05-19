# -------------------------------------------------------------
# code developed by Michael Hartmann during his Ph.D.
# Data Processing: __init__.py
#
# (C) 2021 Michael Hartmann, Graz, Austria
# Released under GNU GENERAL PUBLIC LICENSE
# email michael.hartmann@v2c2.at
# -------------------------------------------------------------
import logging
import cv2
from datareader.source.preprocessing.dataprocessing import *
from datareader.source.util.signalanalysis import *
from datareader.definitions import *
import time
import pandas as pd

'''
    Some parameters
'''
def get_params():
    params=dict()
    params['pre_time_horizon'] = 11
    params['time_horizon'] = 11
    params['window_size'] = 51
    params['polyorder'] = 2
    params['PROJECT_ROOT']=read_project_root
    return params


'''
    Get the project root (see definitions.py)
'''
def read_project_root():
    return get_project_root_pkg()

'''
    Get the dataprocessing object
'''
def get_object(params):
    return dataprocessing(params)

'''
    Read the dataset
'''
def read_dataset(params, path):
    obj = dataprocessing(params)
    X=obj.read_dataset(path)
    return X

'''
   Example function for dataset
'''
def read_dataset_pkg():
    import os
    import datareader
    params = datareader.get_params()
    path = datareader.__path__[0]
    newpath = os.path.join(path, "data/input/stanford/bookstore/video0/annotations.txt")
    X = datareader.read_dataset(params, newpath)
    print(X)

'''
   Get velocity and acceleration for 2D dataset
'''
def get_velocity_for_dataset_2D(dataset, params):
    return get_velocity_signal_for_dataset_2D(dataset, params)

'''
   Get selection of dataset specified by a column and the range from min_val to max_val
   Example: the dataset should be selected by the time range from [4s, 6s]
'''
def get_dataset_by_range(dataset, column, min_val, max_val):
    return dataset_by_range(dataset, column, min_val, max_val)

'''
   Get zonotypes from dataset by a row idx
'''
def get_zonotypes_by_row(dataset, row_idx):
    return get_zonotypes_2D_by_row(dataset, row_idx)

'''
   Get dataset by timestamp
'''
def get_dataset_by_timestamp(dataset, timestamp):
    return get_dataset_by_stamp_by_column(dataset, 't', timestamp)

'''
   Get successor by timestamp for an agent with id
'''
def get_successor_by_timestamp(dataset,timestamp, id):
    #selection by timestamp
    x,a = get_dataset_by_timestamp(dataset, timestamp)
    x,b = get_dataset_by_timestamp(dataset, timestamp+1)
    bool_a, val_a = get_dataset_by_stamp_by_column(a, 'id', id)
    bool_b, val_b = get_dataset_by_stamp_by_column(b, 'id', id)
    if(bool_a==False):
        logging.warn("id not in array at timestamp: " + str(timestamp))
        return 0
    elif(bool_b == False):
        logging.warn("id not in array at timestamp: " + str(timestamp+1))
        return 0
    else:
        return (val_a, val_b)

'''
   Read background image
'''
def read_background_picture(path):
    img = cv2.imread(path, cv2.IMREAD_COLOR)
    RGB_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img

'''
   Plot the background image
'''
def plot_background_picture(name, path):
    img = read_background_picture(path)
    #img=plot_rectangle(img, (5,5), (202,202), (255, 0, 0), 2)
    show(name, img)

'''
   Show image
'''
def show(name, img):
    cv2.imshow(name, img)

'''
   Show image and hold the image
'''
def show_and_hold(name, img):
    cv2.imshow(name, img)
    cv2.waitKey(0)

'''
    plot a rectangle on the image
'''
def plot_rectangle(image, start_point, end_point, color, thickness):
    image = cv2.rectangle(image, start_point, end_point, color, thickness)
    return image

'''
    plot all rectangles on the image for a specific timestamp
'''
def plot_rectangle_for_timestamp(img, dataset, timestamp, color=(255, 0, 0)):
    no, XY = get_dataset_by_timestamp(dataset, timestamp)
    for index, row in XY.iterrows():
        img=plot_rectangle(img, (row['xmin'],row['ymin']), (row['xmax'],row['ymax']), color, 2)
    return img

'''
    plot a polylines
'''
def plot_polylines(image, pts, isClosed, color, thickness):
    image = cv2.polylines(image, [pts], isClosed, color, thickness)
    return image


'''
    get the dataset with a specific value
'''
def get_dataset_by_column_value(dataset, column, value):
    return get_dataset_by_stamp_by_column(dataset, column, value)

'''
    number of the rows in a dataset
'''
def number_of_rows_dataset(dataset):
    return len(dataset.index)
'''
    get center value (x,y)
'''
def get_center_value(dataset):
    t=np.unique(dataset["t"])
    x_erg = []
    y_erg = []
    for i in t:
        act_row=dataset.loc[dataset["t"]==i]
        x_cent = 0.5*(act_row["xmax"].values[0] - act_row["xmin"].values[0])+act_row["xmin"].values[0]
        y_cent = 0.5*(act_row["ymax"].values[0] - act_row["ymin"].values[0])+act_row["ymin"].values[0]
        x_erg.append(x_cent)
        y_erg.append(y_cent)
    return t, np.array(x_erg), np.array(y_erg)

'''
    get values for rectangle for time range
'''
def get_values_rectangle_for_time_range(dataset):
    t=np.unique(dataset["t"])
    x_min_erg = []
    x_max_erg = []
    y_min_erg = []
    y_max_erg = []
    for i in t:
        act_row=dataset.loc[dataset["t"]==i]
        x_min_erg.append(act_row["xmin"].values[0])
        x_max_erg.append(act_row["xmax"].values[0])
        y_min_erg.append(act_row["ymin"].values[0])
        y_max_erg.append(act_row["ymax"].values[0])
    return t, np.array(x_min_erg), np.array(x_max_erg), np.array(y_min_erg), np.array(y_max_erg)

'''
    get extrema of dataset
'''
def get_extrema(dataset):
    return (np.min(dataset["xmin"]), np.max(dataset["xmax"]), np.min(dataset["ymin"]), np.max(dataset["ymax"]))

'''
    get values for rectangle for each row
'''
def get_all_ids(dataset):
    return np.unique(dataset["id"])

'''
    get past data indices for an id for a specific timestamp
'''
def get_past_measurements_indices_for_id(dataset, id, timestamp):
    r, Y=get_dataset_by_column_value(dataset, "id", id)
    bool_vec=Y["t"]<timestamp
    erg=[i for i in bool_vec.index if bool_vec[i]]
    return erg

'''
    get future data for an id for a specific timestamp
'''
def get_future_measurements_for_id(dataset, id, timestamp):
    r, Y=get_dataset_by_column_value(dataset, "id", id)
    bool_vec=Y["t"]>timestamp
    erg=[i for i in bool_vec.index if bool_vec[i]]
    return erg

'''
    get past states from past measurements for a specific id
'''
def get_past_states(dataset, past_id_indices, params, plot_it=False):
    Y=dataset.loc[past_id_indices]
    max_idx_Y=Y.loc[Y['t']==np.max(Y['t'])]
    max_idx_Y=max_idx_Y.iloc[0]
    initial_state_set = np.matrix([[0.5*(max_idx_Y['xmax']-max_idx_Y['xmin']), 0], [0, 0.5*(max_idx_Y['ymax']-max_idx_Y['ymin'])], [0, 0], [0, 0]])
    rt, rx, ry = get_center_value(Y)
    vx, vy=compute_velocity_with_savgol_filter(rx, ry, params["window_size"], params["polyorder"])
    extrema_X = get_extrema(dataset)
    if(plot_it):
        plot_positions_velocities(rt, rx, ry, vx, vy, extrema_X)
    states=[rt, rx, ry, vx, vy]
    initial_state=np.matrix([[rx[-1]], [ry[-1]], [vx[-1]], [vy[-1]]])
    return initial_state, states, initial_state_set

'''
    plot positions and velocities
'''
def plot_positions_velocities(t, px, py, vx, vy, extrema_X):
    f, (ax1, ax2, ax3) = plt.subplots(3, 1)
    ax1.plot(t, px, label='px')
    ax1.plot(t, py, label='py')
    ax1.legend()
    ax2.plot(t, vx, label='vx')
    ax2.plot(t, vy, label='vy')
    ax2.legend()
    ax3.plot(px, py, label='position')
    ax3.axis(extrema_X)
    ax3.legend()
    plt.show()

'''
    get velocity with savgol filter
'''
def compute_velocity_with_savgol_filter(px, py, window_size, polyorder):
    if(len(px)>window_size+2):
        vx = savgol_filter(px, window_size, polyorder, 1)
        vy = savgol_filter(py, window_size, polyorder, 1)
    else:
        return [10, 10], [10, 10]
    return vx, vy

'''
    get future states for a specific id
'''
def get_future_states(dataset, future_id_indices, params, plot_it=False):
    Y=dataset.loc[future_id_indices]
    rt, rx, ry = get_center_value(Y)
    vx, vy=compute_velocity_with_savgol_filter(rx, ry, params["window_size"], params["polyorder"])
    extrema_X = get_extrema(dataset)
    if(plot_it):
        plot_positions_velocities(rt, rx, ry, vx, vy, extrema_X)
    states=[rt, rx, ry, vx, vy]
    return states

'''
    get elapsed time
'''
def get_elapsed_time(init_time):
    elapsed_time = time.time() - init_time
    return elapsed_time

'''
    evaluate and plot computed zonosets from Reachability Analysis and selected dataset
'''
def evaluate_zonoset_selected_dataset(b_dataset, zonoset, extrema_X):
    plt.figure()
    for zoni in zonoset:
        x = zoni[0]
        y = zoni[1]
        plt.fill(x, y, facecolor="green", edgecolor='k', linewidth=3, alpha=.07)
    plot_hull_with_lines(b_dataset)
    plt.axis(extrema_X)
    plt.show()
    None

'''
    plot hull with lines
'''
def plot_hull_with_lines(dataset):
    rt, rxmin, rxmax, rymin, rymax = get_values_rectangle_for_time_range(dataset)
    #################################
    ### computation of velocities ###
    #################################
    plt.plot(rxmin, rymin, 'k')
    plt.plot(rxmax, rymax, 'k')
    [plt.plot([rxmin[i], rxmax[i]], [rymin[i], rymax[i]], 'red') for i in range(0, len(rxmin), 15)]
