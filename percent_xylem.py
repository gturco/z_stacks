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
    pxylem = sum(df[df['Color'] == 'red']['Area'])/ float(sum(df['Area'])) * 100
    ### total number of xylem cells div by total cells
    #pxylem = len(df[df['Color'] == 'red']['Area'])/ float(len(df['Area'])) * 100
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
    header = "percent_xylem\tconc\trep\tVND7\texperiment\tfile_name\n"
    w.write(header)

    for file_name in os.listdir(experiment_dir):
        if file_name.endswith('xls'):
            conc,rep, image = file_name.split("_")
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

            w.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\n".format(pxylem,concint,rep,vnd7,experiment,file_name))
    w.close()

    plot_pxylem("data/experiments/{0}.txt".format(experiment))

#main("test_data/6_4_2017/")
#### This is the first time the experiment was ran
#v = {'0a':1,'01a':8.190654,'02a':73.29085,'1a':204.1371,'2a':934.0905,'10a':1062.62,'20a':1084.355}

vd = {'0a':1,'01a':11.60892342,'02a':115.7867414,'1a':379.431953,'2a':1046.7321,'10a':1635.759087,'20a':1305.488657}

main('/Users/gturco/Documents/Data/VND7-Staining/ClearSee_t/2_41_56/',vd)
#### This is the second experiment ran on all points inbetween
#v  = {'0a':1, '0b':1, '01b':4.243136541,'01a':6.2780298,'013a':11.12606069,'013b':6.341437978,
#        '015a':11.88554756,'015b':9.187026773,'0175b':17.25525048,'02b':0, '02a':0}

#v  = {'0a':1, '0b':1, '01b':4.24,'01a':7.27,'013a':9.5,'013b':7.35,
        #'015a':11.8,'015b':10.65,'0175b':14,'02b':13.15, '02a':9.35}

#v = {'0a':1, '0b':1, '01b':4.24,'01a':7.27,'013a':9.5,'013b':7.35,
#        '015a':11.8,'015b':10.65,'0175b':14,'02b':13.15, '02a':9.35}


#main('/Users/gturco/Documents/Data/VND7-Staining/ClearSee_t/5_10_2017/', v)
####  This was the thrid time the experiment was ran and it was ran on only a subset of the data

#v = {'0a':1,'01a':2.3229,'013a':5.0725722,'015a':6.6161,'2a':3.388,'20a':31.2922}

vz = {'0a':1,'01a':17.96639761,'013a':70.88295844,'015a':70.07699779,'2a':29.38960995,'20a':618.2667755}

main('/Users/gturco/Documents/Data/VND7-Staining/ClearSee_t/7_11_2017/',vz)
#### This is the lower range of concentations
### TODO fix 007 and 075 to correct names for files and in dic


#v = {'001a':3.296760788,'001b':8.209587,'005a':30.48299656,'005b':10.3654,'007a':29.38448454,'007b':20.1641,'01a':0,'01b':0,'013a':0,'013b':0,'075a':0,'075b':0}
#v = {'001a':3.296760788,'001b':5.959,'005a':10.3654,'005b':18.7376,'007a':29.3844,'007b':20.1641,'01a':31.3733,'01b':47.216,'013a':0,'013b':0,'075a':0,'075b':0}
#v = {'001a':3.296760788,'001b':3.296760788,'005a':10.3654,'005b':10.3654,'007a':29,'007b':20,'01a':0,'01b':0,'013a':0,'013b':0,'075a':0,'075b':0}
#v = {'001a':1,'001b':2,'005a':3,'005b':4,'007a':5,'007b':6,'01a':7,'01b':8,'013a':9,'013b':10,'075a':11,'075b':12}
vd = {'007a':55.33496196,'007b':41.25944392,'001a':8.685652026,'001b':10.41265439,'005a':29.59811819,'005b':51.59361902,'01a':62.46997092 ,'01b':63.76059437,'013a':39.73074779,'013b':34.11691644,'075a':189.9563612,'075b':96.04599245}


#

main('/Users/gturco/Documents/Data/VND7-Staining/ClearSee_t/4_1-18/',vd)


