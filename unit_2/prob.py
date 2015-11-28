import scipy.stats as stats
import numpy as np
import matplotlib.pyplot as plt
import collections
import sys


def print_out(str):
    print "{}".format(str)
    sys.stdout.flush()

# Find frequency
def find_frequency(data):
    freq = collections.Counter(data)
    
    # Display collection counter to find mode of data elements
    print_out("DATA POINTS FREQ. TABLE\n{}".format(freq))
    
    # Total sum of data instances
    cnt_sum = sum(freq.values())
    print_out("Total of data instances: {}".format(cnt_sum))
    
    for key, value in freq.iteritems():
        print_out("The frequency of number {} is {}".format(str(key), str(float(value) / cnt_sum)))
        

# Create box plot
def create_boxplot(data):
    plt.figure() 
    plt.boxplot(data)
    plt.savefig("unit2_2_1_boxplot.png")
    
# Create hist plot
def create_histplot(data):
    plt.figure()
    plt.hist(data, histtype='bar')
    plt.savefig("unit2_2_1_histplot.png")

# Create QQ plots with test data
def create_qqplots(data):
    plt.figure() # New figure    
    test_data = np.random.normal(size=1000)   
    graph1 = stats.probplot(test_data, dist="norm", plot=plt)
    plt.savefig("unit2_2_1_qq_normalplot.png") #this will generate the first graph
    
    plt.figure()
    test_data2 = np.random.uniform(size=1000)   
    graph2 = stats.probplot(test_data2, dist="norm", plot=plt)
    plt.savefig("unit2_2_1_qq_uniformplot.png") #this will generate the second graph
    
    # Using the data to see if it looks like any of the distributions above
    plt.figure()  
    graph2 = stats.probplot(data, dist="norm", plot=plt)
    plt.savefig("unit2_2_1_qq_data.png") #this will generate the third graph
        
if __name__ == '__main__':
    
    # Data definition
    data = [1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 4, 4, 4, 4, 5, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 9, 9]
    
    # Display element counts and frequency distribution
    find_frequency(data)
    
    # Create box plots
    create_boxplot(data)
    
    # Create hist plots
    create_histplot(data)
    
    # Create QQ plots with sample random data
    create_qqplots(data)
    
    

