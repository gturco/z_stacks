import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os

def get_percent_xylem(file_name):
    """ gets percentage xylem from image assumes all boxes are labled as either red or blue or yellow"""
    ### read file into pandas
    df = pd.read_table(file_name)
    ### total area of blue marked cells/ xylem indicated div by total area marked as root * 100
    pxylem = sum(df[df['Color'] == 'blue']['Area'])/ sum(df[df['Color'] != 'yellow']['Area']) * 100
    return pxylem



def plot_pxylem(pxylem_data):

    xylem_data = pd.read_table(pxylem_data)


    # Initialize the figure
    f, ax = plt.subplots(figsize=(7, 6))
    #ax.set_xscale("log")

    # Plot the orbital period with horizontal boxes
    sns.boxplot(x="conc", y="percent_xylem", data=xylem_data,
            whis=np.inf, palette="vlag")

    # Add in points to show each observation
    sns.swarmplot(x="conc", y="percent_xylem", data=xylem_data,
              size=6, color=".3", hue="experiment", linewidth=0)


    # Make the quantitative axis logarithmic
    ax.xaxis.grid(True)
    ax.set(ylabel="")
    sns.despine(trim=True, left=True)
    plt.show()

def main(experiment_dir):
    """go through imageJ dir and find percentage of root that is xylem from 
    each annotated image and plot datapoints"""
    experiment = experiment_dir.split('/')[-2]

    w = open("data/experiments/{0}.txt".format(experiment),'wb')
    header = "percent_xylem\tconc\texperiment\n"
    w.write(header)

    for file_name in os.listdir(experiment_dir):
        if file_name.endswith('xls'):
            ### get vars from file names
            conc, image = file_name.split("_")
            ### get the concentation of estradiol from the experiment
            if conc.startswith('0') and len(conc) > 1:
                conc = float(conc.replace('0','.', 1))
            else: conc = float(conc)
            # read file into pandas and get percent xylem
            pxylem = get_percent_xylem(experiment_dir + file_name)

            w.write("{0}\t{1}\t{2}\n".format(pxylem,conc,experiment))
    w.close()

    plot_pxylem("data/experiments/{0}.txt".format(experiment))

main("test_data/6_4_2017/")
