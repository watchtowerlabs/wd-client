# -*- coding: utf-8 -*-

from observer import observer


def start_new_observer(tle, observation_window, frequency):
    """ Initialises and starts a new observer and exits
    """
    new_observer = observer()
    if new_observer.setup(tle, observation_window['end'], frequency):
        new_observer.observe()
