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
    pxylem = sum(df[df['Color'] == 'red']['Area'])/ sum(df['Area']) * 100
    return pxylem



def plot_pxylem(pxylem_data):

    xylem_data = pd.read_table(pxylem_data)


    # Initialize the figure
    f, ax = plt.subplots(figsize=(7, 6))
    #ax.set_xscale("log")

    # Plot the orbital period with horizontal boxes
    sns.boxplot(x="VND7", y="percent_xylem", data=xylem_data,
            whis=np.inf, palette="vlag")

    # Add in points to show each observation
    sns.swarmplot(x="VND7", y="percent_xylem", data=xylem_data,
              size=6, color=".3", linewidth=0)


    # Make the quantitative axis logarithmic
    ax.xaxis.grid(True)
    ax.set(ylabel="")
    sns.despine(trim=True, left=True)
    plt.show()

def main(experiment_dir, v):
    """go through imageJ dir and find percentage of root that is xylem from 
    each annotated image and plot datapoints"""
    experiment = experiment_dir.split('/')[-2]

    w = open("data/experiments/{0}.txt".format(experiment),'wb')
    header = "percent_xylem\tconc\trep\tVND7\texperiment\n"
    w.write(header)

    for file_name in os.listdir(experiment_dir):
        if file_name.endswith('xls'):
            conc, rep, image = file_name.split("_")

            ### get the concentation of estradiol from the experiment
            if conc.startswith('0') and len(conc) > 1:
                concint = float(conc.replace('0','.', 1))
            else: concint = float(conc)

            ### if we have the fold change values input them otherwise just plot the est conctraction
            if len(v) > 0:
                vnd7 = v[conc+rep]
            else: vnd7 = concint
            # read file into pandas and get percent xylem
            print file_name
            pxylem = get_percent_xylem(experiment_dir + file_name)

            w.write("{0}\t{1}\t{2}\t{3}\t{4}\n".format(pxylem,concint,rep,vnd7,experiment))
    w.close()

    plot_pxylem("data/experiments/{0}.txt".format(experiment))

#main("test_data/6_4_2017/")
#### This is the first time the experiment was ran
#v = {'0a':1,'01a':8.190654,'02a':73.29085,'1a':204.1371,'2a':934.0905,'10a':1062.62,'20a':1084.355}
#main('/Users/gturco/Documents/Data/VND7-Staining/ClearSee/2_41_56/',v)
#### This is the second experiment ran on all points inbetween
#v  = {'0a':1, '0b':1, '01b':4.243136541,'01a':6.2780298,'013a':11.12606069,'013b':6.341437978,
#        '015a':11.88554756,'015b':9.187026773,'0175b':17.25525048,'02b':15.25050493, '02a':9.357021518}
#main('/Users/gturco/Documents/Data/VND7-Staining/ClearSee/5_10_2017/', v)
####  This was the thrid time the experiment was ran and it was ran on only a subset of the data
#v = {'0a':1,'01a':8.53,'013a':17.50,'015a':13.096,'2a':14.317,'20a':1.57}
#main('/Users/gturco/Documents/Data/VND7-Staining/ClearSee/7_11_2017/',v)
#### This is the lower range of concentations
v = {}
main('/Users/gturco/Documents/Data/VND7-Staining/ClearSee/4_1-18/',v)


