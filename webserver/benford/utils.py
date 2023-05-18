from collections import defaultdict


def get_lead_digits_frequencies(file):
    # Creating a dictionary with default values
    frequency_digit_counts = defaultdict(int)

    number_obs = -1
    # Reading all observed values line per line:
    for line in file:
        # skipping header
        if number_obs < 0:
            number_obs = 0
            continue
        
        # Check that each line has at least one column: 
        values = line.split()
        if len(values) < 1:
            raise Exception("Failed to extract digit in file. This file has a missing value in line: " + line)
        
        # Checking that value in the last column is an integer:
        obs_value = values[-1].decode("utf-8")
        if not obs_value.isnumeric():
            raise Exception("Failed to extract digit in file. Value is not an integer: " + obs_value)

        frequency_digit_counts[ str(int(obs_value))[0] ] += 1
        number_obs += 1

    # Computing frequencies in percent of each digit from 1 to 9, into an array of size 9:
    lead_digit_freq_percent = [0] * 9
    for digit in frequency_digit_counts.keys():
        lead_digit_freq_percent[int(digit)-1] = (float(frequency_digit_counts[digit]) / float(number_obs) ) * 100.0

    return number_obs, lead_digit_freq_percent
