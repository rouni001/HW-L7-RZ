from collections import defaultdict
from typing import List, Optional 

import matplotlib.pyplot as plt
import numpy as np
import base64


def get_lead_digits_frequencies(file):
    """Returns the frequencies of lead digits 
    Args:
        file: An UploadedFile object.

    Returns:
        (number_obs, lead_digit_freq_percent): 
            Number of observations found in 'file',
            Array (of size 9) for the frequencies for each lead digit (in percent)
    """
    # Creating a dictionary handling automatically default values
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
            raise Exception(
                "Failed to extract digit: Missing value at the last column, in line number {}.".
                format(number_obs + 2)
            )
        
        # Checking that value in the last column is an integer:
        obs_value = values[-1].decode("utf-8")
        if not obs_value.isnumeric():
            raise Exception(
                "Failed to extract digit: Value [{}] is not an integer in line number {}.".
                format(obs_value, number_obs + 2)
            )

        frequency_digit_counts[ str(int(obs_value))[0] ] += 1
        number_obs += 1

    # Creating an array of integers, with default value 0.    
    lead_digit_freq_percent = [0] * 9
    # Computing frequencies in percent for each digit from 1 to 9:
    for digit in frequency_digit_counts.keys():
        lead_digit_freq_percent[int(digit)-1] = (float(frequency_digit_counts[digit]) / float(number_obs) ) * 100.0

    return number_obs, lead_digit_freq_percent


def create_paired_bars_figure(
    left_distr: List[float], 
    right_distr: List[float], 
    file_path: str, 
    x_axis_title: str,
    y_axis_title: str,
    fig_title: str,
    left_lbl_legend: str,
    right_lbl_legend: str,
    right_bars_color: Optional[str] = "green",
    x_axis_start_label: int = 1,
) -> str:
    """Create a figure of grouped bars for the Expected/Observed distributions. 
    Args:
        left_distr (List[float]:    Expected distribution to plot on the left
        right_distr (List[float]:   Observed distribution to plot on the right
        file_path (str):            File path to store the image
        x_axis_title (str):         x-axis title
        y_axis_title (str):         y-axis title
        fig_title (str):            Title of the figure
        left_lbl_legend (str):      Name of the expected distribution in the legend
        right_lbl_legend (str):     Name of the observed distribution in the legend
        right_bars_color (Optional[str]):
                                    Color of the bars representing the observed data. 
                                    Default value: green,
        x_axis_start_label (int). Default value: 1.
                                    Start value of the bars x-axis values.

    Returns:
        image_data: The two-bars graph figure converted in text.
    """
    if len(left_distr) == 0:
        raise Exception("Failed to plot distributions: Expected data are empty")

    if len(right_distr) == 0:
        raise Exception("Failed to plot distributions: Observed data is empty.")

    if len(left_distr) != len(right_distr):
        raise Exception("Failed to plot distribution: Sizes of Expected and Observed data do not match.")
    
    x_axis = np.arange(x_axis_start_label, x_axis_start_label + len(right_distr), 1) 
    plt.switch_backend('Agg') 
    
    fig = plt.figure(figsize = (8, 5))
    plt.bar(x_axis-0.2, left_distr, color="blue", width = 0.4)
    plt.bar(x_axis+0.2, right_distr, color=right_bars_color, width = 0.4)
    
    plt.xlabel(x_axis_title)
    plt.ylabel(y_axis_title)
    plt.title(fig_title)
    plt.legend([left_lbl_legend , right_lbl_legend])
    plt.xticks(x_axis)
    plt.savefig(file_path)

    # Encode plotted image as text
    with open(file_path, "rb") as image_file:
        image_data = base64.b64encode(image_file.read()).decode('utf-8')

    return image_data
