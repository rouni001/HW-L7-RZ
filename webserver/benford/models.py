from benford.utils import get_lead_digits_frequencies
from scipy.stats import chisquare

import numpy as np
import matplotlib.pyplot as plt
import base64


# Expected Frequency Distribution in Benford's Law (BL)
BENFORD_EXP_DIST = [
    30.0, 
    18.0,
    12.0,
    10.0,
    8.0,
    7.0,
    6.0,
    5.0,
    4.0,
]

# Critical value at 5% significance level for the Chi-Square distribution (DF=8)
CHI_SQUARE_CRITIAL_VALUE = 15.51


class BenfordLawFitnessAnalyzer:
    def __init__(self, frequencies) -> None:
        chisquare_test = chisquare(frequencies, f_exp=BENFORD_EXP_DIST)
        self.chi_square_statistic = chisquare_test.statistic

    def is_null_hypothesis_rejected(self) -> bool:
        return self.chi_square_statistic > CHI_SQUARE_CRITIAL_VALUE

    
# Create your models here.
class ObservedDataAnalyzer:
    def __init__(self, file) -> None:
        self.filename = file.name[:-4]
        self.error_message = None
        self.statistical_test_analyser = None
        self.number_observations = None
        self.lead_digits_frequencies = None
        self.is_data_unnatural = None
        self.plot_image = None

        self.run_statistical_test(file)
        self.plot_distribution()

    def run_statistical_test(self, file) -> None:
        if self.statistical_test_analyser is None or file is None:
            try:
                self.number_observations, self.lead_digits_frequencies = get_lead_digits_frequencies(file)
            except Exception as e:
                self.error_message = str(e)
                return
            self.statistical_test_analyser = BenfordLawFitnessAnalyzer(self.lead_digits_frequencies)
            self.is_data_unnatural = self.statistical_test_analyser.is_null_hypothesis_rejected()

    def is_data_valid(self) -> None:
        return self.error_message is None

    def plot_distribution(self) -> None:
        if not self.is_data_valid():
            return
        if self.plot_image is None:
            plot_file_path = "webserver/benford/static/results.png"

            color = "maroon" if self.is_data_unnatural else "green"
            x_axis = np.arange(1, 10, 1) 
            plt.switch_backend('Agg') 
            
            fig = plt.figure(figsize = (8, 5))
            plt.bar(x_axis-0.2, BENFORD_EXP_DIST, color="blue", width = 0.4)
            plt.bar(x_axis+0.2, self.lead_digits_frequencies, color=color, width = 0.4)
            
            plt.xlabel("Lead Digit")
            plt.ylabel("Frequencies")
            plt.title("Expected vs Observed Frequencies of Lead Digits")
            plt.legend(["Benford Law", self.filename])
            plt.xticks(x_axis)
            plt.savefig(plot_file_path)

            # Encode plot image as text
            with open(plot_file_path, "rb") as image_file:
                image_data = base64.b64encode(image_file.read()).decode('utf-8')

            self.plot_image = image_data
