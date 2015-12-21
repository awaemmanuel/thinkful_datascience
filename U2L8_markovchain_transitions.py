import pandas as pd
'''
    Helper matrix for dot matrix
'''
def matrix_dot(A, B):
    return A.dot(B)

def multi_matrix_dot(A, B, num=1):
    for _ in range(num):
        A = matrix_dot(A, B)
    return A

# Create indexes of the transition matrix
indexes = ['Bull market', 'Bear market', 'Stagnant market']

stocks = pd.DataFrame({'Bull market': [.9, .15, .25,], 
                       'Bear market': [.075, .8, .25], 
                       'Stagnant market': [.025, .05, .5]}, 
                      index = indexes)

# First markov transition
print "FIRST TRANSITION PROBABILITY: \n", stocks


# Second order transtion
stock_2 = stocks.dot(stocks)
print "SECOND TRANSITION PROBABILITY: \n", stock_2

# After 5 Transitions.
stocks_5 = multi_matrix_dot(stocks, stocks, 5)
print "FIFTH TRANSITION PROBABILITY: \n", stocks_5


# After 10 Transitions.
stocks_10 = multi_matrix_dot(stocks, stocks, 10)
print "TENTH TRANSITION PROBABILITY: \n", stocks_10

# After 20 Transitions.
stocks_20 = multi_matrix_dot(stocks, stocks, 20)
print "TWENTY TRANSITION PROBABILITY: \n", stocks_20

# After 25 Transitions.
stocks_25 = multi_matrix_dot(stocks, stocks, 25)
print "TWENTY FIFTH TRANSITION PROBABILITY: \n", stocks_25

# After 30 Transitions.
stocks_30 = multi_matrix_dot(stocks, stocks, 30)
print "THIRTY TRANSITION PROBABILITY: \n", stocks_30

# After 40 Transitions.
stocks_40 = multi_matrix_dot(stocks, stocks, 40)
print "FORTY TRANSITION PROBABILITY: \n", stocks_40


'''
    We start to notice a convergence at about 45 transitions.
    Meaning at this point we near our steady state.
'''

# After 45 Transitions.
stocks_45 = multi_matrix_dot(stocks, stocks, 45)
print "FORTY-FIFTH TRANSITION PROBABILITY: \n", stocks_45

# After 47 Transitions.
stocks_47 = multi_matrix_dot(stocks, stocks, 47)
print "FORTY-SEVENTH TRANSITION PROBABILITY: \n", stocks_47

# After 50 Transitions.
stocks_50 = multi_matrix_dot(stocks, stocks, 50)
print "FIFTY TRANSITION PROBABILITY: \n", stocks_50

# After 100 Transitions.
stocks_100 = multi_matrix_dot(stocks, stocks, 100)
print "HUNDREDTH TRANSITION PROBABILITY: \n", stocks_100

# Can you a name some real-life examples that could be modeled by Markov chains?
print "Examples of Markov Chains in real-life are:\n1. Dice board games.\n2. A random walking agent in a simulated environment.\n3. Weather Prediction\n4. Lexical construction in NLP.\n5. Spam and virus detection and so on.\n"


# Can you name examples that cannot be treated as Markov chains?
print "We cannot treat things that transition from state to state without randomization. If the transtion is known or deterministic, then we cannot model it as a Markov Chain. Examples are:\n1. Days of the week.\n2. Months of the year.\n"


# Can you name an example of finite probabilistic states that cannot be modeled as Markov chains?
print "A 'discrete time stochastic process' is an example of a finite probabilistic state that cannot be modeled as a Markov chain. Because transitions in Markov chains are completely described by probability and transition probabilities can only depend on current state."

