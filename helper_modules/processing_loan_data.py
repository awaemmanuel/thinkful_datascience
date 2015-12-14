import re, string
import numpy as np

def remove_pattern_from(array_of_strings, pattern=''):
    return map(lambda text: re.sub(pattern, '', str(text)), array_of_strings)

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

def convert_nan_to_zero(list_of_values):
    for idx, val in enumerate(list_of_values):
        if np.isnan(val):
            list_of_values[idx] = 0
    return list_of_values
