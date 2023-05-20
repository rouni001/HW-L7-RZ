from benford.utils import get_lead_digits_frequencies, create_paired_bars_figure 
from scipy.stats import chisquare


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

# Default p-value for the Chi-Square distribution
CHI_SQUARE_P_VALUE_PERCENT = 5
# Critical value at 5% significance level for the Chi-Square distribution (DF=8)
CHI_SQUARE_CRITIAL_VALUE = 15.51


class BenfordLawFitnessAnalyzer:
    def __init__(self, frequencies) -> None:
        chisquare_test = chisquare(frequencies, f_exp=BENFORD_EXP_DIST)
        self.chi_square_statistic = chisquare_test.statistic
        self.critical_value = CHI_SQUARE_CRITIAL_VALUE
        self.p_value = CHI_SQUARE_P_VALUE_PERCENT

    def is_null_hypothesis_rejected(self) -> bool:
        return self.chi_square_statistic > CHI_SQUARE_CRITIAL_VALUE

    
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
            self.plot_image = create_paired_bars_figure(
                BENFORD_EXP_DIST,
                self.lead_digits_frequencies,
                "webserver/benford/static/results.png",
                "Lead Digit",
                "Frequencies (%)",
                "Expected vs Observed Frequencies of Lead Digits",
                "Benford Law",
                self.filename,
                "maroon" if self.is_data_unnatural else "green",
                1
            )
