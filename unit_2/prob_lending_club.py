import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats


# Read csv data from url and drop empty rows inplace
loans = pd.read_csv('https://spark-public.s3.amazonaws.com/dataanalysis/loansData.csv')
loans.dropna(inplace=True)

'''
    Create plots
    i.e One new figure for each plot to avoid plot overlapping.
    
    1. Boxplot
    2. Histplot
    3. QQ Plots
'''

# 1
plt.figure()
loans.boxplot(column = 'Amount.Funded.By.Investors')
plt.savefig('unit2_2_loansboxplot.png')

# 2
plt.figure()
loans.hist(column = 'Amount.Funded.By.Investors')
plt.savefig('unit2_2_loanshistplot.png')

# 3
plt.figure()
graph = stats.probplot(loans['Amount.Funded.By.Investors'], dist = 'norm', plot = plt)
plt.savefig('unit2_2_qq_loansplot.png')


