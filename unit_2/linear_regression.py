import pandas as pd
import re
import matplotlib.pyplot as plt

# Read data from cvs file
loansData = pd.read_csv('https://spark-public.s3.amazonaws.com/dataanalysis/loansData.csv')

# Drop null rows
loansData.dropna(inplace=True)

def remove_pattern_from(array_of_strings, pattern=''):
    return map(lambda text: re.sub(pattern, '', text), array_of_strings)

def processs_interest_rates(list_of_loan_rates):
    try:
        pattern = re.compile(r'%')
        interest_rates = map(lambda rate: round((float(rate) / 100), 4), remove_pattern_from(list_of_loan_rates, pattern))
        return interest_rates
    except TypeError:
        raise TypeError('Please check the type of input')

def process_loan_lengths(list_of_loan_lengths):
    pattern = re.compile(r' months')
    clean_loan_length = map(lambda length: int(length), remove_pattern_from(list_of_loan_lengths, pattern))
    return clean_loan_length

def convert_fico_range_to_score(fico_range_strs):
    fico_range_strs = fico_range_strs.strip().split('-')
    fico_scores = [int(score) for score in fico_range_strs]
    return fico_scores[0]


# Clean up Interest Rate. Remove % sign, convert str -> float and find decimal representation.
clean_interest_rates = processs_interest_rates(loansData['Interest.Rate'])
loansData['Interest.Rate'] = clean_interest_rates

# Clean up the Loan Lengths. i.e Remove the months in the string and convert it to int
clean_loan_lengths = process_loan_lengths(loansData['Loan.Length'])
loansData['Loan.Length'] = clean_loan_lengths


# Clean up FICO ranges and convert them to FICO Scores. Creata a new column in DataFrame using Series and original index
loansData['FICO.Score'] = pd.Series(map(convert_fico_range_to_score, loansData['FICO.Range']), index = loansData.index)

# Plot figures
plt.figure()
loansData['FICO.Score'].hist()
plt.savefig('fico_score_hist.png')
plt.clf() # Clear old plot

# Default scatter matrix plot
a = pd.scatter_matrix(loansData, alpha=0.05, figsize=(10,10))
plt.savefig('data_loan_scatter_matrix_1.png')
plt.clf()

# Scatter matrix plot with histogram of data plots in the diagonal
a = pd.scatter_matrix(loansData, alpha=0.05, figsize=(10,10), diagonal='hist')
plt.savefig('data_loan_scatter_matrix_2.png')
plt.clf()
