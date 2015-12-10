import pandas as pd
import statsmodels.api as sm
import numpy as np
import matplotlib.pyplot as plt

'''
    Helper Function: Return 0 for interest rate < 12 and 1 otherwise.
'''
def classify_interest_rates(interest_rate):
    return 1 if interest_rate < 0.12 else 0
        
'''
    Determine the probability of getting a loan given a FICO Score and loan amount
'''
def logistic_function(fico_score, loan_amt, coeff):
    try:
        offer_loan = 0
        prob =  np.exp(coeff['Intercept'] + (coeff['FICO.Score'] * fico_score) + (coeff['Amount.Requested'] * loan_amt))/(1 + np.exp(coeff['Intercept'] + (coeff['FICO.Score'] * fico_score) + (coeff['Amount.Requested'] * loan_amt)))
        if prob > 0.7:
            offer_loan = 1
        return prob, offer_loan
    except Exception as e:
        raise Exception(e)

'''
    Determine automatically if we will get a loan amount given a FICO Score
'''
def pred_range(fico_range, coeff, amt_requested=10000):
    data_points = []
    decisions = []
    for score in fico_range:
        prob, decision = logistic_function(score, amt_requested, coeff)
        data_points.append(prob)
        decisions.append(decision)
    return data_points, decisions

'''
    Predicting if one gets the loan automatically
'''
def will_get_loan(fico_score, amt_requested=10000):
    global coeff
    return True if logistic_function(fico_score, amt_requested, coeff)[1] == 1 else False
        

# Load data into panda DataFrame
loansData = pd.read_csv('loansData_clean.csv')

# Create new columns: Interest binary classifications and intercept for logistic regression
loansData['IR_TF'] = pd.Series(map(classify_interest_rates, loansData['Interest.Rate']), index = loansData.index)

loansData['Intercept'] = pd.Series(1.0, index = loansData.index)

# List of independent variables
ind_vars = ['Intercept','FICO.Score', 'Amount.Requested']

# Define the logist regression function
logit = sm.Logit(loansData['IR_TF'], loansData[ind_vars])

# Fit the model
model = logit.fit()
coeff = model.params

# Get the fitted coefficients from the results.
print "Model Parameters: \n", coeff


prob, offer_loan = logistic_function(750, 10000, coeff)

print "Probability of getting ${} with a FICO Score of {} for an interest rate < 12% is: {}%".format(10000, 750, round(prob * 100, 3))

prob, p = logistic_function(720, 10000, coeff)
print "Probability of getting ${} with a FICO Score of {} for an interest rate < 12% is: {}%".format(10000, 720, round(prob * 100, 3))

print "Sam has a FICO score of {} and needs a loan of {}. Will he get the loan?: {}".format(780, 13000, 'YES' if will_get_loan(780, 13000) else 'NO')

# Plot the decision of different FICO Score decisions for a loan request of $10,000. 
fico_range = np.linspace(600, 850) # Actual range is 301, but who will give you $10k with anything below 600
prob_data, decisions = pred_range(fico_range, coeff)

plt.figure(figsize=(20, 15))
plt.plot(fico_range, prob_data, label = 'p(x) = exp(b+mx)/(1+exp(b+mx))', color = 'blue') 
plt.hold(True)
plt.plot(fico_range, decisions, 'ro', label = 'Decision for 10000 USD')
plt.legend(loc='upper right')
plt.xlabel('Fico Scores')
plt.ylabel('Probability and decision, yes = 1, no = 0')
plt.savefig('probability_of_getting_loan.png')