# -------------------------------------------------------------
# code developed by Michael Hartmann during his Ph.D.
# Data Processing
#
# (C) 2021 Michael Hartmann, Graz, Austria
# Released under GNU GENERAL PUBLIC LICENSE
# email michael.hartmann@v2c2.at
# -------------------------------------------------------------

import argparse
import definitions
from __init__ import *
import logging
def test():
    #############################
    ###     initial steps     ###
    #############################
    params=get_params()
    path = datareader.__path__[0]
    location="bookstore"
    video="video0"
    annotation_path = os.path.join(path, "data/input/stanford/", location, video, "annotations.txt")
    image_path = os.path.join(path, "data/input/stanford/", location, video, "reference.jpg")
    ################################
    ###     read the dataset     ###
    ################################
    X = read_dataset(params, annotation_path)
    logging.info(X)
    #################################
    ### read the dataset by range ###
    #################################
    Y=get_dataset_by_range(X, 't', 8520, 8531)
    logging.info(Y)
    ##############################
    ### get velocity by filter ###
    ##############################
    Z = get_velocity_for_dataset_2D(X, params)
    logging.info(Z)
    ##################################
    ### zonotype of a specific row ###
    ##################################
    XX=get_zonotypes_by_row(Z, 0)
    logging.info(XX)
    ###############################
    ### dataset for a timestamp ###
    ###############################
    a, XY=get_dataset_by_timestamp(Y, 8524)
    logging.info(XY)
    ########################################
    ### get successor for next timestamp ###
    ########################################
    XZ=get_successor_by_timestamp(Y, 8524, 2)
    logging.info(XZ)
    #######################################
    ### plot background reference image ###
    #######################################
    #plot_background_picture(location+"_"+video, image_path)
    ###############################################
    ### plot rectangles for a specific timstamp ###
    ###############################################
    img = read_background_picture(image_path)
    img=plot_rectangle_for_timestamp(img, Y, 8524)
    #show_and_hold("", img)
    #############################################
    ### get all initial states from timestamp ###
    #############################################
    ###########################################
    ### get all future rectangles of agents ###
    ###########################################


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--window_x', '-wix', type=int, help='windowsize in x-direction for savgol_filter', default=101,
                        required=False)
    parser.add_argument('--window_y', '-wiy', type=int, help='windowsize in y-direction for savgol_filter', default=101,
                        required=False)
    parser.add_argument('--poly_x', '-pox', type=int, help='polygon order in x-direction for savgol_filter', default=2,
                        required=False)
    parser.add_argument('--poly_y', '-poy', type=int, help='polygon order in y-direction for savgol_filter', default=2,
                        required=False)
    args = parser.parse_args()
    params = vars(args)
    params['PROJECT_ROOT'] = definitions.get_project_root_pkg()
    test()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    main()