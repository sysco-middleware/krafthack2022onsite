from msilib.schema import Class
from importlib_metadata import NullFinder
import matplotlib.pyplot as plt
import numpy as np
from scipy.fftpack import fft
from scipy import signal
import tkinter as tk
from tkinter import filedialog
import pathlib
from pathlib import Path
import os
import time
import librosa
import IPython.display as ipd
from librosa import display
import pandas as pd

class DataSetSplitting:
    def __init__(self,folder:str):
        self.folder: str = folder
        self.dataframe: pd.DataFrame = None
    def loadFile(self) -> None:
        cwd = Path.cwd()
        file_path = Path(cwd).joinpath(r'Unit4', 'input_dataset-2.parquet')
        self.dataframe = pd.read_parquet(file_path)

    def fixFileForBolt(self,boltNumber:str, isVibration:bool):
        # no neet for reactive power and vibrations
        ColumnsToDrop = ['Unit_4_Reactive Power']
        if isVibration == False:
            ColumnsToDrop.append('lower_bearing_vib_vrt')
            ColumnsToDrop.append('turbine_bearing_vib_vrt')
        
        DfColumns = [ x for x in list(self.dataframe.columns) if x not in ColumnsToDrop or 'Tensile' in x or 'Torsion' in x]
        DfColumns.append(f"{boltNumber}_Torsion")
        DfColumns.append(f"{boltNumber}_Tensile")
        BoltXDf = self.dataframe[DfColumns].copy()
        BoltXDf = BoltXDf.dropna(subset=[f"{boltNumber}_Torsion", f"{boltNumber}_Tensile"])
        BoltOperationdf = BoltXDf.drop(BoltXDf[BoltXDf['mode'] == 'start'].index)
        BoltOperationdf = BoltOperationdf.drop(columns = ['mode'],axis=1)
        BoltStartdf = BoltXDf.drop(BoltXDf[BoltXDf['mode'] == 'operation'].index)
        BoltStartdf = BoltStartdf.drop(columns = ['mode'],axis=1)
        BoltStartdf.to_csv(f"{self.folder}/{boltNumber}Dataset2Start.csv", index=False)
        BoltOperationdf.to_csv(f"{self.folder}/{boltNumber}Dataset2Operation.csv", index=False)

if __name__ == "__main__":
    dst = DataSetSplitting('Unit4')
    dst.loadFile()
    for i in range(1,7):
        dst.fixFileForBolt(f"Bolt_{i}",False)

