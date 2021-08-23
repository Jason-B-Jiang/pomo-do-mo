#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : Jason Jiang
# Created Date: August 16, 2021
# Last Updated: August 22, 2021
# version = 0.0
# ---------------------------------------------------------------------------

"""This module provides the class for the main Pomo-do-mo application window.
"""

# ---------------------------------------------------------------------------

# Imports
from __future__ import annotations
import tkinter as tk
from tkinter import *

from Buttons import _Button
from Timers import _Timer
from InputBoxes import _WorkTimeInput, _BreakTimeInput


def _is_valid_time(s: str) -> bool:
    """Returns whether a user-inputted time is a valid integer number of
    minutes, that is greater than zero.

    Credit to https://note.nkmk.me/en/python-check-int-float/ for this
    function code

    >>> _is_valid_time('ooooo')
    False
    >>> _is_valid_time('90')
    True
    >>> _is_valid_time('29.20023')
    False
    >>> _is_valid_time('0')
    False
    >>> _is_valid_time('-23.4')
    False
    """
    try:
        tmp = float(s)

    except ValueError:
        return False  # s wasn't an int, or float coercible to int

    else:  # check if float is coercible to int
        return tmp.is_integer() and tmp > 0


class PomodomoApp(tk.Tk):
    """Main app for the Pomo-do-mo' timer.

    I should finish writing this docstring...
    """

    def __init__(self) -> None:
        # Let Pomodomo_app inherit all attributes of a Tkinter root window
        super().__init__()

        # Set root window title, size and color
        self.title("Pomo-do-mo'!")
        self.geometry('425x275')  # fix window size
        self.maxsize(425, 275)
        self.minsize(425, 275)
        self.config(bg='white')  # make window background white

        # Create a work timer and break timer object
        self.work_timer = _Timer(self)
        self.break_timer = _Timer(self)

        # Create input fields for user to specify work time and break time
        # Default text in input fields is default work/break times
        self.work_time_input = _WorkTimeInput(self)
        self.break_time_input = _BreakTimeInput(self)

        self.work_timer.set_time(self.work_time_input.get_user_input())
        self.break_timer.set_time(self.break_time_input.get_user_input())

        # Create buttons to start/pause the app, and to reset the timers and
        # stop the app
        self.start_and_pause_button = _Button(self, 'Start/pause',
                                              self.start_or_pause_pomodomo_session)
        self.reset_button = _Button(self, 'Reset',
                                    self.reset_pomodomo_session)
        self.reset_button.disable_button()  # initialize button as disabled

        # Set bool attributes to indicate if the pomodomo timer has ever been
        # started (i.e: the start button has been hit at least once), and
        # whether the timer is currently counting down

        # Note to self: if started is False, then paused must be False as well,
        # but not the other way around
        self.started = False
        self.paused = False

        # add labels to on-screen elements, get rid of this later...
        self.work_timer_label = Label(self, text='WORK', bg='white')
        self.break_timer_label = Label(self, text='BREAK', bg='white')
        self.work_input_label = Label(self,
                                      text='Enter work time (minutes):',
                                      bg='white')
        self.break_input_label = Label(self,
                                       text='Enter break time (minutes):',
                                       bg='white')

        # Pack all the widgets onto the screen
        self.work_timer.grid(row=0, column=1)
        self.work_timer_label.grid(row=0, column=0)
        self.break_timer.grid(row=1, column=1)
        self.break_timer_label.grid(row=1, column=0)
        self.work_time_input.grid(row=2, column=1)
        self.work_input_label.grid(row=2, column=0)
        self.break_time_input.grid(row=3, column=1)
        self.break_input_label.grid(row=3, column=0)
        self.start_and_pause_button.grid(row=4, column=1)
        self.reset_button.grid(row=5, column=1)

    def start_or_pause_pomodomo_session(self) -> None:
        """Starts or pauses the countdown of the work and break timers,
        when the 'Start / Pause' button is pressed.
        """
        if not self.started:
            # Set user inputted times into work and break timers
            input_work = self.work_time_input.get_user_input()
            input_break = self.break_time_input.get_user_input()

            work_timer_setup = self.work_timer.set_time(input_work)
            break_timer_setup = self.break_timer.set_time(input_break)

            if work_timer_setup and break_timer_setup:
                self.started = True

                # start countdown loop, after a 1 second delay to prevent the
                # first second from counting down immediately
                self.after(1000, self._pomodomo_countdown_loop)

                # disable the entry boxes for work and break time when the
                # pomodomo app has started
                self.work_time_input.disable_input()
                self.break_time_input.disable_input()

                # enable the reset button
                self.reset_button.enable_button()

            else:
                # TODO - make this a pop-up message for the user
                print("Invalid work/break time input. Please enter an integer.")

        # User pressed start/stop button again after it was started, so pause
        # execution of the pomodomo countdown loop
        elif not self.paused:
            self.paused = True
            self.after_cancel(pomodomo_loop)  # end the countdown loop

        else:  # App had started, and was paused
            self.paused = False  # unpause the pomodomo app
            self.after(1000, self._pomodomo_countdown_loop)  # restart loop

    def reset_pomodomo_session(self) -> None:
        """Stops countdown of the work and break timers, and resets the
        work and break timers back to the starting work/break times.
        """
        # Note to self: if reset button is clickable, then started MUST be true
        assert self.started
        self.started = False
        self.paused = False
        self.reset_button.disable_button()

        self.work_time_input.enable_input()
        self.break_time_input.enable_input()

        # reset work and break timers to initial starting times
        self.work_timer.reset_time_left()
        self.break_timer.reset_time_left()

    def _pomodomo_countdown_loop(self) -> None:
        """Starts counting down work time and break time, continuing this
        countdown loop until the user hits the stop button.

        Countdown stops when user pauses the timer, or stops it entirely.
        """
        if self.started and not self.paused:

            # Time left on work_timer, so count down on that timer
            if self.work_timer.get_time_left() != '0:00:00':
                self.work_timer.countdown()

            # Time left on _break_timer, so count down on that timer
            elif self.break_timer.get_time_left() != '0:00:00':
                self.break_timer.countdown()

            # work_timer and _break_timer have both hit zero, so reset them
            # for another Pomodoro work cycle
            else:
                self.work_timer.reset_time_left()
                self.break_timer.reset_time_left()

            # Make the countdown loop a global variable, so it can easily
            # be stopped by self.after_cancel
            global pomodomo_loop
            pomodomo_loop = self.after(1000, self._pomodomo_countdown_loop)

        else:  # App was paused or reset, so stop the timer countdown loop
            return
