#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : Jason Jiang
# Created Date: August 16, 2021
# Last Updated: August 22, 2021
# version = 0.0
# ---------------------------------------------------------------------------

"""This module provides a timer class, to help track of and display work and
break times for the Pomo-do-mo application."""

# ---------------------------------------------------------------------------

# Imports
from __future__ import annotations

import datetime
import tkinter as tk
from tkinter import Label


def _is_valid_time(s: str) -> bool:
    """Returns whether a user-inputted time is a non-negative and non-zero
    integer or float.

    >>> _is_valid_time('ooooo')
    False
    >>> _is_valid_time('90')
    True
    >>> _is_valid_time('0.5')
    False
    >>> _is_valid_time('0')
    True
    >>> _is_valid_time('-23.4')
    False
    """
    try:
        return s.isdigit() and int(s) >= 0

    except ValueError:
        return False  # s wasn't an int or a float


class _Timer(Label):
    """An abstract Label subclass, providing an interface for the work time
    and break time timer widgets.

    === Private attributes ===
    _time_set: A datetime.timedelta object indicating the work/break time set
    by the user

    _time_left: A datetime.timedelta object indicating how much work/break time
    is left in a given Pomodoro cycle.

    === Representational invariants ===
    - _time_set is a valid, non-zero time in datetime.timedelta
    - _time_left is a valid, non-zero time in datetime.timedelta
    - datetime.timedelta(seconds = 0) <= _work_time_left <= _work_time
    """
    _time_set: datetime.timedelta
    _time_left: datetime.timedelta

    def __init__(self, root: tk.Tk) -> None:
        # Treat _WorkTimer as a normal Label object, setting font to size 48
        # Arial, with black font color and white background.
        Label.__init__(self, root, font=('Arial', 48), fg='black',
                       bg='white')

        # Initialize _time_set to 0 mins, and set _time_left to be the zero mins
        self._time_set = datetime.timedelta(minutes=0)
        self._time_left = self._time_set

        # Finally, set the label text of _Timer to _time_left
        self.config(text=str(self._time_left))

    def get_set_time(self) -> str:
        """Returns the string of self._time_set.
        """
        return str(self._time_set)

    def get_time_left(self) -> str:
        """Returns the string of self._time_left.
        """
        return str(self._time_left)

    def reset_time_left(self) -> None:
        """Set _time_left back to _time_set.
        """
        self._time_left = self._time_set
        self.config(text=str(self._time_set))

    def set_time(self, input_time: str) -> bool:
        """Takes user-inputted time from the work/break time entry box
        widget, and updates self._time_set, self._time_left, as well
        as the label text to reflect this new input time.

        Returns True if user-inputted time was a valid number and _Timer
        object was successfully updated, and False otherwise.
        """
        # Take inputted work time from an entry widget, set label to that
        # amount of time, and set _time_set and _time_left to that time

        # check if user-inputted time is a valid number
        if not _is_valid_time(input_time):
            return False

        # convert user-inputted time to minutes
        minutes = int(float(input_time))

        # if user-inputted time (in minutes) >= 60, convert to hours and get
        # overflowing minutes from the hour
        hours = 0  # Initialize hours as zero
        if minutes >= 60:
            hours = minutes // 60  # Get hours from minutes if >= 60 mins
            minutes = minutes % 60  # Get overflowing minutes from hour

        new_work_time = datetime.timedelta(hours=hours, minutes=minutes)

        # Update _work_time and _work_time_left to the new user-inputted work
        # time, and change text of the _WorkTime object to reflect the new
        # work time
        self._time_set = new_work_time
        self._time_left = new_work_time
        self.config(text=str(new_work_time))

        # Finally, return True to indicate input time was valid and _WorkTimer
        # successfully updated
        return True

    def countdown(self) -> None:
        """Subtracts one second from _time_left, and updates the on-screen
        label text of the _WorkTime object to reflect the new _time_left.
        """
        self._time_left -= datetime.timedelta(seconds=1)
        self.config(text=str(self._time_left))
