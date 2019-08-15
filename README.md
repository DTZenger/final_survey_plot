# final_survey_plot

This project contains groups of files for stave assembly to quickly visualize and check to see the survey indicates a module is placed incorrectly.

## Getting Started

You will need to have LabView 2016 edition to run the vi programs included correctly.
For python, you will need python3.6 or better to be able to run these programs. Packages needed are numpy, matplotlib, pandas, and glob (glob2)

## Which file to use:
All most up to date vi programs are in the folder 'Todd'. Included are the vi programs and the python scripts that these vi programs call on.

## The python files:

### final_survey_plot.py:

This file can be used to accomplish three objectives: 
* Plot the relative (ideal positions - actual survey positions) X and Y seperate histograms and saves them in a specified directory.
* Get database relative positions for each module and corner. It gives a dictionary of a module where the keys are the corners and they contain a list of the relative X and Y values.
* Get database quick statistics for each module: quickly tells if X and/or Y is off more than a tolerance value (default value is 1mm). It also tells you how many X and Y modules have failed

You will need to provide the script with an ideal placement csv and survey placement csv. You can place additional comments in these csv valuse by starting the line with a # symbol.

The csv files must have the data in the following format:
```
Modlue-1-A-x,Module-1-A-y,Module-1-A-z
Modlue-1-B-x,Module-1-B-y,Module-1-B-z
Modlue-1-C-x,Module-1-C-y,Module-1-C-z
Modlue-1-D-x,Module-1-D-y,Module-1-D-z
Modlue-2-A-x,Module-2-A-y,Module-2-A-z
...
```
