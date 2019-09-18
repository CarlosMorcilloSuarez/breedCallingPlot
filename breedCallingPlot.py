#!/usr/bin/env python3 	
# -*- coding: utf-8 -*-


'''breedCallingPlot.py

'''

__author__ = "Carlos Morcillo-Suarez"
__license__ = "GPL"
__version__ = "2019/09/18 11:55" # YYYY/MM/DD HH:MM
__email__ = "carlos.morcillo.upf.edu@gmail.com"


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
                         "breeds=","colors=","help"]
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
        elif opt in ("--colors"):
            global colorsFileName            
            colorsFileName = arg
        elif opt in ("--help"):
            usage()
            sys.exit(-1)        
    return(args)
    
def usage():
    print()
    print('''
    
       breedCallingPlot.py
        
           Creates a genomic plot of a chromosome showing the breed
           assigned to each fragment for one or more breed discovery
           experiments.
           
                
       SYNOPSIS
        
            python breedCallingPlot.py [options] file [file2] [file3]...
        
                              
       OPTIONS
                                       
            --output <file_name>
                    File name of the generated plot.
                    Default value: 'breedCallingPlot.png'                    
                    
            --legend <legend>
                    Description of the plot.
                    
            --chromosome <chromosome_label>
                    Label of the plotted chromosome.
                    
            --breeds <breeds_file>
                    Name of a file containing the list of breeds to be plotted.
                    When plotting a single experiment, the breeds file can
                    be omited.
                  
             --colors <colors_file>
                    Name of a file containing the list of colors to be used
                    when plotting the breed calls for every experiment. If
                    the list of colors is shorter than the list of experiments
                    then colors are rotated from the beginning.
                    
             --help
                    Shows this help information.
                    
       FILES
         
            List of files containing each one the calls of a breed discovery
            experiment.
           
           
       DEPENDENCIES
        
            numpy
            pandas
            matplotlib
            genomePlot
                https://github.com/CarlosMorcilloSuarez/genomePlot           
            
    ''')    
    
    
if __name__ == "__main__":

    # Globals
    inputFileNames = []
    outputFileName = 'breedCallingPlot.png'
    breedsFileName = ''
    colorsFileName = ''
    chromosome=''    
    legend = ''
        
    # Process command line
    inputFileNames = processArguments(sys.argv[1:])    

    if inputFileNames == []:
        print("Input file name not specified - Exiting")
        print()
        print("--help for further information")
        sys.exit(-1)
        
    if breedsFileName == '' and len(inputFileNames) != 1:
        print("When plotting more than one calls file", end=' ')
        print("Breeds file has to be provided - Exiting")
        print()
        print("--help for further information")
        sys.exit(-1)
        
    if colorsFileName == '':
        colors = ['#1f77b4']
    else:
        with open(colorsFileName,'r') as colorsFile:
            colors = [color.strip() for color in list(colorsFile)]
            
    isFirstFile = True
    counter = 0
    opacity = 1/len(inputFileNames)
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
        color = colors[counter % len(colors)]
        for index, row in list(calls.iterrows())[1:]:
            x_Pos = initialPosition
            y_Pos = breeds.index(row.Breed)+1.1
            ax.add_patch(Rectangle(
                                  (x_Pos,y_Pos),row.Position-initialPosition,0.8,
                                  zorder = 1,
                                  alpha = opacity,
                                  facecolor = color
                                  )
                         )
            initialPosition = row.Position 
            
        isFirstFile = False
        counter += 1
    fig.savefig(outputFileName)
    
