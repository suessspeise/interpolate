import numpy as np
import scipy.interpolate
import matplotlib.pyplot as plt
import csv
import sys

# interpolate plot from:
# https://stackoverflow.com/questions/17577587/matplotlib-2d-graph-with-interpolation#17578793

def load_csv(filename):
    x = []
    y = []
    t = []
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print(row)
            x.append(row['x'])
            y.append(row['y'])
            t.append(row['t'])
        
# reads .txt spectrum file, returns (2,n)-np.array, n = length of file - header 
def load_txt(filename):
    num_head_lines = 1 # length of header
    # load txt-file, get number of rows
    crs = open(filename, "r")
    rows = (row.strip().split() for row in crs)
    num_lines = sum(1 for line in open(filename))

    next_row = next(rows) # ommit header
    # put in list
    x = []; y = []; t = [] # empty lists
    for i in range(num_lines - 1):
        next_row = next(rows) # get next
        if next_row != []: # append if not empty
            x.append(float(next_row[0]))
            y.append(float(next_row[1]))
            t.append(float(next_row[2]))
        else:
            print(i, " empty")
    # convert to np.arrays  
    x = np.asarray(x)
    y = np.asarray(y)
    t = np.asarray(t)
    # return as (2,n)-np.array
    return np.vstack((x,y,t))
        

def main():
    decke = load_txt("decke3.txt")
    #plt.scatter(decke[0], decke[1])
    xi, yi = np.mgrid[decke[0].min():decke[0].max():500j, decke[1].min():decke[1].max():500j]
    #xi, yi = np.mgrid[-4.0:4.0:500j, 0.0:13.0:500j]
    a_rescale = rescaled_interp(decke[0], decke[1], decke[2], xi, yi)
    #a_orig = normal_interp(decke[0], decke[1], decke[2], xi, yi)
    #plot(decke[0], decke[1], decke[2], a_orig, 'Not Rescaled')
    plot(decke[0], decke[1], decke[2], a_rescale, 'Rescaled')
    plt.show()

def normal_interp(x, y, a, xi, yi):
    rbf = scipy.interpolate.Rbf(x, y, a)
    ai = rbf(xi, yi)
    return ai

def rescaled_interp(x, y, a, xi, yi):
    a_rescaled = (a - a.min()) / a.ptp()
    ai = normal_interp(x, y, a_rescaled, xi, yi)
    ai = a.ptp() * ai + a.min()
    return ai

def plot(x, y, a, ai, title):
    fig, ax = plt.subplots()

    im = ax.imshow(ai.T, origin='lower',
                   extent=[x.min(), x.max(), y.min(), y.max()])
                   #extent=[-4.0, 4.0, 0.0, 13.0])
    ax.scatter(x, y, c=a)

    ax.set(xlabel='X', ylabel='Y', title=title)
    fig.colorbar(im)


main()    
