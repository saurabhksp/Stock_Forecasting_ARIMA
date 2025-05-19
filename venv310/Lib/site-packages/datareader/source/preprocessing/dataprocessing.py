# -------------------------------------------------------------
# code developed by Michael Hartmann during his Ph.D.
# Data Processing: Pre-Processing
#
# (C) 2021 Michael Hartmann, Graz, Austria
# Released under GNU GENERAL PUBLIC LICENSE
# email michael.hartmann@v2c2.at
# -------------------------------------------------------------

from datareader.source.util.signalanalysis import *
from datareader.source.util.helpfunctions import *
import os
from pathlib import Path

'''
Class dataprocessing:

A) IDEA: Get datasets like Stanford Drone Dataset and provide functionality for data-processing
'''
class dataprocessing(object):
    def __init__(self, params, **kwargs):
        self.ROOT_DIR = str(params['PROJECT_ROOT'])

    '''
    Test-function
    '''
    def test(self, params):
        self.file_path = self.readInputDataTxt()
        self.dataset = self.readDataset(params)
        #param2DataFrame = gettingAlgorithmicParams(self.ROOT_DIR)
        # self.dataDict=self.computeDataDict(params, param2DataFrame)
        self.dataset = self.datasetWithProcessing(params)
        self.extremePositions = self.getExtrema()

    """
        get the whole dataset depending on the path variable and get a pandas variable back
    """
    def read_dataset(self, path):
        df = pd.read_csv(path, sep=" ", header=None,
                         names=['id', 'xmin', 'ymin', 'xmax', 'ymax', 't', 'lost', 'occluded', 'generated', 'label'])
        # data = pd.read_csv(self.file_path, header=None)
        return df

    """
        get the whole dataset depending on the path variable and get a pandas variable back
    """
    def preprocessing_dataset(self, params, dataset):
        knowledgeDataset = get_velocity_for_dataset_2D(dataset, params)
        return knowledgeDataset
