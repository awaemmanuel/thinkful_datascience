import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import statsmodels.api as sm
from sklearn.metrics import mean_squared_error

# Set seed for reproducible results
np.random.seed(414)

# Gen toy data
X = np.linspace(0, 15, 1000)
y = 3 * np.sin(X) + np.random.normal(1 + X, .2, 1000)

# results and data
train_X, train_y = X[:700], y[:700]
test_X, test_y = X[700:], y[700:]

train_df = pd.DataFrame({'X': train_X, 'y': train_y})
test_df = pd.DataFrame({'X': test_X, 'y': test_y})
new_X = sm.add_constant(test_X)

# Linear Fit
poly_1 = smf.ols(formula='y ~ 1 + X', data=train_df).fit()
pred_y = poly_1.predict(new_X, transform=False)
r1 = mean_squared_error(test_y, pred_y)

# Quadratic Fit
poly_1 = smf.ols(formula='y ~ 1 + X + I(X**2)', data=train_df).fit()
pred_y = poly_1.predict({'X': test_X})
r2 = mean_squared_error(test_y, pred_y)

print """
Comparing MSE: 
Quadratic fit MSE : {}
Linear fit MSE : {}
""".format(r1, r2)