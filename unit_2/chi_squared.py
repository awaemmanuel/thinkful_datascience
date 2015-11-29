import scipy.stats as stats
import matplotlib.pyplot as plt
import collections
import pandas as pd

# Load the reduced version of the Lending Club Dataset
loans = pd.read_csv('https://spark-public.s3.amazonaws.com/dataanalysis/loansData.csv')

# Clean data in place. Drop null rows
loans.dropna(inplace=True)

freq = collections.Counter(loans['Open.CREDIT.Lines'])

# Calculate the chi-squared distribution
chi, p = stats.chisquare(freq.values())

print "The chi-squared is {} and p-value is {}".format(round(chi, 3), p)