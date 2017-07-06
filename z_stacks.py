import matplotlib.pyplot as plt
import os
import sys
from czifile import CziFile
import numpy as np


def read_czi(czi_path):
    with CziFile(czi_path) as czi:
        image_arrays = czi.asarray()
    return image_arrays


def get_files(image_dir):
     for root, dirs, files in os.walk(image_dir, topdown=True): 
        #print(dirs)
        files = [f for f in files if not f[0] == '.']
        dirs[:] = [d for d in dirs if not d[0] == '.']
        yield root, files

        
def generate_figure(images):
    # To fit on the screen in a nice way, we can arange the 
    # z-stack in a grid of 6x3 on a large figure.
    images.sort(key=lambda tup: tup[0])
    N_rows = 3
    N_cols = 4
    
    
    for index,image in enumerate(images):
        plt.subplot(N_rows,N_cols,index+1)
        plt.imshow(image[1])
        plt.title(image[0])
    plt.show()

def get_fold_change(z_stack, image_arrays):
    
    lignin = []
    cellulose = []
        
    for index in range(z_stack):
        lignin.append((np.sum(image_arrays[0,1,0,index]),index))
        cellulose.append((np.sum(image_arrays[0,0,0,index]),index))

    lignin.sort(key=lambda x: x[0])
    cellulose.sort()
        
    return lignin[-1][0], cellulose[-1][0],lignin[-1][1], cellulose[-1][1]
    
    
    
def main(image_dir, reps):
    experiment = image_dir.split("/")[-2]
    all_dirs = list(get_files(image_dir))
    l_images= []
    c_images= []
    for path, files in all_dirs:
        est_conc = path.split("/")[-1]
        rep = "a"
        if reps:
            est_conc =  path.split("/")[-2]
            rep = path.split("/")[-1].lower()

        for image_file in files:
            if image_file.endswith("czi"):
                file_number = image_file.strip(".czi")
                czi_path = path + "/" + image_file
                image_arrays = read_czi(czi_path)
                z_stack = len(image_arrays[0,0,0])
                if z_stack > 2:
                    l_value, c_value, l_index, c_index = get_fold_change(z_stack,image_arrays)
                    image_size = len(image_arrays[0,0,0,1]) * float(len(image_arrays[0,0,0,1]))
                    print "{0},{1},lignin,{2},{3},{4},{5}".format(est_conc,l_value/image_size, experiment , file_number, len(image_arrays[0,0,0,1]),rep)
                    print "{0},{1},cellulose,{2},{3},{4},{5}".format(est_conc,c_value/image_size, experiment, file_number, len(image_arrays[0,0,0,1]),rep)
                    l_images.append((float(est_conc),image_arrays[0,1,0,l_index].T[0]))
                    c_images.append((float(est_conc),image_arrays[0,0,0,c_index].T[0]))
    print len(l_images)
    generate_figure(l_images)
    generate_figure(c_images)

            
#print list(get_files("/Users/gturco/Documents/Data/VND7-Staining/ClearSee/2_41_56/"))
main("/Users/gturco/Documents/Data/VND7-Staining/ClearSee/2_41_56/", False)

#main("/Users/gturco/Documents/Data/VND7-Staining/ClearSee/5_10_2017/", True)
## Name so it orders better...
## concentration, fold change, value, lignin/cellulose , experiment, file_number
## get experiment, file number
## number of rows and cols

## fold change
## raw value
## experiment - date
## top or bottom - put in myself

## plot concentraction verse raw values
## plot concentraction verse raw values
## color code vrs top or bottom
