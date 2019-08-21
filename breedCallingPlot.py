#!/usr/bin/env python3 	
# -*- coding: utf-8 -*-


'''breedCallingPlot.py

'''

__author__ = "Carlos Morcillo-Suarez"
__license__ = "GPL"
__version__ = "2019/08/21 17:06" # YYYY/MM/DD HH:MM
__email__ = "carlos.morcillo.upf.edu@gmail.com"
__copyright__ = "Copyright 2018, Carlos Morcillo-Suarez"


import sys


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import getopt

from genomePlot import createsGenomePlot


def processArguments(argv):
    try:
        opts, args = getopt.getopt(
                        argv,
                        "",
                        ["chromosome=", "legend=","output=",
                         "breeds="]
        )

    except getopt.GetoptError as e:
        print(e)
        sys.exit(2)
    for opt, arg in opts:        
        if opt in ("--output"):
            global outputFileName
            outputFileName = arg
        elif opt in ("--legend"):
            global legend
            legend = arg
        elif opt in ("--chromosome"):
            global chromosome
            chromosome = arg
        elif opt in ("--breeds"):
            global breedsFileName
            breedsFileName = arg
    return(args)
    
if __name__ == "__main__":

    # Globals
    inputFileNames = []
    outputFileName = 'breedCallingPlot.png'
    breedsFileName = ''
    chromosome=''    
    legend = ''
        
    # Process command line
    inputFileNames = processArguments(sys.argv[1:])    
    if inputFileNames == []:
        print("Input file name not specified - Exiting")
        sys.exit(-1)
    if breedsFileName == '' and len(inputFileNames) != 1:
        print("When plotting more than one calls file", end=' ')
        print("Breeds file has to be provided - Exiting")
        sys.exit(-1)
    
    isFirstFile = True
    opacity = 1/len(inputFileNames)
    color = 'black'
    for inputFileName in inputFileNames:
        
        # Reads input File
        data = pd.read_csv(inputFileName,sep='\t',header=None)
        chromosomes = [coordinate.split(':')[0] for coordinate in data[0]]
        positions = [int(coordinate.split(':')[1]) for coordinate in data[0]]
        data.insert(loc=0, column='Position', value=positions)
        data.insert(loc=0, column='Chromosome', value=chromosomes)
        data = data.drop(columns=[0])
        data.columns = ['Chromosome','Position','Breed']
        calls = data
        
        if isFirstFile:
            if breedsFileName:
                breeds = list(pd.read_csv(breedsFileName,header=None)[0])[::-1]
            else:            
                breeds = sorted(list(set(data.Breed)))[::-1]
        
            xWidth = list(calls.Position)[-1]
            yScale = len(breeds)+1            

            # Figure
            fig = plt.figure(figsize=(14,8),dpi=300)

            # title plot
            ax_title = fig.add_axes([0,0.9,1,0.1])
            ax_title.axis("off")
            fontsize = 12
            ax_title.text(0.05,0.6,'Calling: ',
                         fontsize = fontsize)
            ax_title.text(0.17,0.6,legend,
                         fontsize = fontsize,
                         color = '#1f77b4')
            ax_title.text(0.05,0.30,'Chromosome: ',
                         fontsize = fontsize)
            ax_title.text(0.17,0.30,chromosome,
                         fontsize = fontsize,
                         color = '#1f77b4')
                         
            # main plot
            ax = fig.add_axes([0.2,0.1,0.7,0.8])

            ## Creates Genome Plot with genomic coordinates
            createsGenomePlot(ax,
                              chromosome=chromosome,
                              xOrigin = -1,
                              xWidth = xWidth,
                              yScale = yScale
                             )

            ax.set_yticks([])
            ax.spines['left'].set_visible(False)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.set_title('') # Eliminates the title created with createsGenomePlot

            ## Plots Breed names 
            xPosition = -list(calls.Position)[-1] / 50
            for index,breed in enumerate(breeds):
                ax.text(xPosition,index+1.5,breed,
                       horizontalalignment = 'right',
                       verticalalignment = 'center')
                if index % 3 == 0:
                    ax.axhline(y = index+1.5,
                               color='#ddddff',
                               linewidth = 1,
                               zorder = 0
                               ) 

        ## Plots Calls
        initialPosition = list(calls.Position)[0]
        for index, row in list(calls.iterrows())[1:]:
            x_Pos = initialPosition
            y_Pos = breeds.index(row.Breed)+1.1
            ax.add_patch(Rectangle(
                                  (x_Pos,y_Pos),row.Position-initialPosition,0.8,
                                  zorder = 1,
                                  alpha = opacity,
                                  #color = color
                                  )
                         )
            initialPosition = row.Position
            
        isFirstFile = False
    fig.savefig(outputFileName)
    
