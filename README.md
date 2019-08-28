# breedCallingPlot

Creates a genomic plot of a chromosome showing the breed assigned to each fragment for one or more breed discovery experiments.

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
           
           
           
