import pickle


def loadPlotFrameSettingsFromFile(filename):
    f = open(filename, 'r')
    retval = pickle.load(f)
    f.close()
    return retval


def savePlotFrameSettingsToFile(settings, filename):
    f = open(filename, 'wb+')
    pickle.dump(settings, f)
    f.close()


class PlotFrameSettings(object):
    """
    This class holds the settings necessary to start a PlotFrame talking to a
    specific host and port and what values to subscribe to.
    """
    def __init__(self, host="localhost", port=5055, subscriptions=[],
                 subplots={}, n_points=2500):
        """
        host is the Publisher of data
        port is the TCP port on which to communicate
        subscriptions is a list of datasets to request from the far side. The
            values are strings like 'time' or 'body.height'
        subplots is a dictionary saying what should be plotted vs. what.  Items
            are (x_axis_data_name, y_axis_data_name) pairs, like ('time',
            'body.height')
        n_points is the number of points to display for a data series
        """
        self.host          = host
        self.port          = port
        self.subscriptions = subscriptions
        self.subplots      = {}
        self.n_points      = 500
