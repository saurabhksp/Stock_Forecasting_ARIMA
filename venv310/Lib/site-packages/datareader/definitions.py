# -------------------------------------------------------------
# code developed by Michael Hartmann during his Ph.D.
# Data Processing
#
# (C) 2021 Michael Hartmann, Graz, Austria
# Released under GNU GENERAL PUBLIC LICENSE
# email michael.hartmann@v2c2.at
# -------------------------------------------------------------

import os
import datareader
def get_project_root_pkg():

    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    return ROOT_DIR