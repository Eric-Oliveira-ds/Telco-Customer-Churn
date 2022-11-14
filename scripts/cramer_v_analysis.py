from scipy.stats import chi2_contingency
import numpy as np
import pandas as pd


def cramers_V(var1,var2) -> float:
    """ Function calculate a relation with two nominal variables
        Receive:
            var1 - one nominal variable for first 
            var2 - one nominal variable for second
        Return:
            number - float value with cramer v relation
    """
  # Cross table building
    crosstab = np.array(pd.crosstab(var1,var2, rownames=None, colnames=None)) 
  # Keeping of the test statistic of the Chi2 test
    stat = chi2_contingency(crosstab)[0] 
  # Number of observations
    obs = np.sum(crosstab) 
  # Take the minimum value between the columns and the rows of the cross table
    mini = min(crosstab.shape)-1 

    return (stat/(obs*mini))