# Not yet thoroughly tested

from time_sources import global_time

class Filter(object):
    """
    Abstract base class for first order signal filters. Do not call directly.
    The init method is overridden by subclasses in order to calculate
    filter constants.
    """

    def _test_update(self, signal):
        """
        Increments time by 10 ms and then calculates the response.
        """
        global_time.updateDelta(0.01)
        return self.update(signal)

    def update(self, signal):
        """
        Calculate and return response.
        """
        # If this is the first signal, update signal and response history,
        # then return the signal as the response
        if not hasattr(self, 'last_response'):
            self.last_signal = signal
            self.last_response = signal
            return float(signal)

        a, b, c = self.a, self.b, self.c # Filter constants
        time_delta = global_time.getDelta()

        # First order filter implementation
        out = (self.last_response + \
               (a + b * time_delta) * signal - \
               a * self.last_signal) / (1.0 + c * time_delta)

        # Update history
        self.last_response = out
        self.last_signal = signal
        return out

class LowPassFilter(Filter):
    def __init__(self, gain, corner_frequency):
        """
        Calculate FOF constants for a low pass filter.
        """
        super(LowPassFilter, self).__init__()
        self.a = 0.
        self.b = gain * corner_frequency
        self.c = corner_frequency

class HighPassFilter(Filter):
    def __init__(self, gain, corner_frequency):
        """
        Calculate FOF constants for a high pass filter.
        """
        super(HighPassFilter, self).__init__()
        self.a = gain
        self.b = 0.
        self.c = corner_frequency

class ZPKFilter(Filter):
    def __init__(self, gain, pole_frequency, zero_frequency):
        """
        Calculate FOF constants for a high pass filter.
        """
        super(ZPKFilter, self).__init__()
        self.a = gain * pole_frequency / zero_frequency
        self.b = gain * pole_frequency
        self.c = pole_frequency

class IntegratorFilter(Filter):
    def __init__(self, gain):
        """
        Calculate FOF constants for a integrator filter.
        """
        super(IntegratorFilter, self).__init__()
        self.a = 0.
        self.b = gain
        self.c = 0.



