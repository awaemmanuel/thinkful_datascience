from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm

# Read the data
df = pd.read_csv('LoanStats3b.csv', header = 1, low_memory=False)

# Change issue column to Date time object
df['issue_d_format'] = pd.to_datetime(df['issue_d'])

# Make a series and group the columns by year/month
dfts = df.set_index('issue_d_format')
year_month_summary = dfts.groupby(lambda x: x.year * 100 + x.month).count()
loan_count_summary = year_month_summary['issue_d']

# Plot the loan amount
plt.figure(figsize = (10, 5))
plt.plot(loan_count_summary)
plt.savefig("raw_loan_cnt_summary.png")
plt.clf()

print "Is it STATIONARY - It's not stationary time series. There's an upward trend (constant decay) in loan count over time. To obtain a stationary time series, we need to differenced series, from this to get another that's stationary. As ARIMA assumes the time series is stationary, we need to get this stationary series before performing ACF and PACF"


# Find loan count summary's first differential
loan_count_summary_diffed = loan_count_summary.diff()

# The first row will be NaN, and maybe others, so we want to fill NaNs with 0
loan_count_summary_diffed = loan_count_summary_diffed.fillna(0)

# Taking a look at a sample plot, we see that there are negative values. Hence we need to smoothen it out

plt.plot(loan_count_summary_diffed)
plt.savefig("diffed_loan_cnt_summary.png")
plt.clf()

'''
    Plot shows some negative values, so we add this difference back to the original series for regression
    We got the threshold from the minimum value of the series.
'''

summary_diff_and_thres = loan_count_summary_diffed + 380
plt.plot(summary_diff_and_thres)
plt.savefig("diff_and_thres_loan_cnt_summary.png")
plt.clf()

"""  we can even smooth it out by diving with the maximum value """

summary_diff_and_thres = summary_diff_and_thres/max(summary_diff_and_thres)

plt.plot(summary_diff_and_thres)
plt.savefig("smooth_diff_and_thres_summary.png")

""" Plot out the ACF and PACF"""
sm.graphics.tsa.plot_acf(summary_diff_and_thres) 
plt.savefig("acf.png")
plt.clf()
sm.graphics.tsa.plot_pacf(summary_diff_and_thres)
plt.savefig("pacf.png")
plt.clf()
            
print "From the ACF/PACF plots, we notice a gradually decaying autocorrelations and a persistent partial autocorrelations. It implies that the model is best served by MA terms to match the lags of significant autocorrelations."