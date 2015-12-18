import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
import numpy as np
import matplotlib.pyplot as plt

from helper_modules import processing_loan_data as pld

# Load data into pandas
df = pd.read_csv('LoanStats3a.csv')


# Clean up Interest Rate. Remove % sign, convert str -> float and find decimal representation.
clean_interest_rates = pld.processs_interest_rates(df['int_rate'])
clean_interest_rates = pld.convert_nan_to_zero(clean_interest_rates)
df['int_rate'] = clean_interest_rates

# Clean up Annual Income
clean_income = df['annual_inc']
clean_income = pld.convert_nan_to_zero(clean_income)
clean_income = np.log1p(clean_income)
df['annual_inc'] = np.log1p(clean_income)


'''
    Clean up Home ownership
    See the unique category labels. [nan 'MORTGAGE' 'NONE' 'OTHER' 'OWN' 'RENT']
    We can use pd.Categorical to get [-1  0  1  2  3  4], 
    but then nan is categorized too and done alphabetical. Hence we categorize using 
    simple list comprehension.
    i.e Naturally order it as ['OWN', 'MORTGAGE', 'RENT', 'OTHER', 'NONE/NAN']
''' 

# Clean home_ownership.
home_ownership = df.home_ownership
print np.unique(home_ownership) 

home_ownership = [4 if x == 'OWN' else 3 if x == 'MORTGAGE' else 2 if x == 'RENT' else 1 if x == 'OTHER' else 0 for x in home_ownership]
df['home_ownership'] = home_ownership

print np.unique(home_ownership) 

# Plots
plt.figure(figsize = (10, 5))
plt.scatter(df.int_rate, df.annual_inc, alpha = 0.5)
plt.xlabel('Interest Rate')
plt.ylabel('Annual Income')
plt.savefig('int_vs_income.png')

# Create an interaction column of log income and homeownership
df['income_and_ownership'] = [ x * y for x, y in zip(df['annual_inc'].tolist(), df['home_ownership'].tolist())]

# Analysis - Stacking of columns seems buggy.
y = np.array(df['int_rate'])
x = df[['annual_inc', 'home_ownership', 'income_and_ownership']]
X = x.as_matrix()

print "USING SM.OLS ANALYSIS\n"
model = sm.OLS(y, X).fit()
print model.summary()
