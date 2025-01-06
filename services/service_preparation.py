import numpy as np

def get_noise_amplitude_value_for_percentage(percentage):
    """
    Computes the noise amplitude for a given percentage.

    Params:
        - percentage (int, 1-100)

    Returns:
        The noise amplitude, a value in the range [0, 2pi]
    """
    if percentage < 0 or percentage > 100:
        raise Exception("Percentages must be between 0 and 100")
    return 2 * np.pi * (percentage/100)