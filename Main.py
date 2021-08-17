#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : Jason Jiang
# Created Date: August 16, 2021
# version = 0.0
# ---------------------------------------------------------------------------

"""This module provides the main Tkinter window for Pomo-do-mo, as well as
classes for all of the widgets in the window (timers, input boxes, buttons)."""

# TODO:
# 1) Make a parent class for _WorkTimer and _BreakTimer, and have them inherit
#    most of their methods from there
#
# 2) Make a parent class from _StartStopButton and _ResetButton, since they are
#    very similar
#
# 3) Make a parent class for _WorkTimeInput and _BreakTimeInput, since these
#    classes are very similar
#
# 3) Keep track of how many Pomodoro cycles a user has worked through in a
#    single session of using the app, and how much time they've worked
#
# 4) Create a pop-up window telling users to input valid number of minutes into
#    the entry boxes, when an invalid input is given
#
# 5) Separate each the button, timer, input and main app classes into their own
#    modules
#
# KNOWN BUGS:
# - Rapidly pausing/unpausing the timers can cause the app to crash;
#   may disable start/stop button briefly after it is pressed to fix this
#
# ---------------------------------------------------------------------------

# Imports
from __future__ import annotations

import datetime
import tkinter as tk
from tkinter import *


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


class _WorkTimer(Label):
    """A Label subclass for keeping track of how much time the user works in
    a single Pomodoro cycle, in PomodomoApp. Also creates a label widget on the
    PomodomoApp window to show how much work time a user has left.

    === Private attributes ===
    _root: The PomodomoApp tkinter window that _WorkTimer belongs to.

    _work_time: A datetime.timedelta object indicating how long the user works
    for, in a single Pomodoro cycle.

    _work_time_left: A datetime.timedelta object tracking how much time a user
    has left to work, in a given Pomodoro cycle.

    === Representational invariants ===
    - _root is an instance of PomodomoApp
    - _work_time is a valid, non-zero time in datetime.timedelta
    - _work_time_left is a valid, non-zero time in datetime.timedetla
    - datetime.timedelta(seconds = 0) <= _work_time_left <= _work_time
    """
    _root: PomodomoApp
    _work_time: datetime.timedelta
    _work_time_left: datetime.timedelta

    def __init__(self, root: PomodomoApp) -> None:
        """Initializes an instance of _WorkTimer.

        >>> p = PomodomoApp()
        >>> wt = _WorkTimer(p)
        >>> wt._root == p
        True
        >>> wt._work_time == datetime.timedelta(minutes = 25)
        True
        >>> wt._work_time_left == wt._work_time
        True
        >>> wt['text'] == str(wt._work_time_left)
        True
        """
        self._root = root

        # Treat _WorkTimer as a normal Label object, setting font to size 48
        # Arial, with black font color and white background.
        Label.__init__(self, root, font=('Arial', 48), fg='black',
                       bg='white')

        # Initialize _work_time to 25 minutes, and _work_time_left to 25
        # minutes as well
        self._work_time = datetime.timedelta(minutes=25)
        self._work_time_left = self._work_time

        # Finally, set the label text of _WorkTime to _work_time_left
        self.config(text=str(self._work_time_left))

    def get_work_time(self) -> str:
        """Returns the string of self._work_time.

        >>> p = PomodomoApp()
        >>> wt = _WorkTimer(p)
        >>> wt.get_work_time()
        '0:25:00'
        """
        return str(self._work_time)

    def get_work_time_left(self) -> str:
        """Returns the string of self._work_time_left.

        >>> p = PomodomoApp()
        >>> wt = _WorkTimer(p)
        >>> wt.get_work_time_left()
        '0:25:00'
        """
        return str(self._work_time_left)

    def reset_time_left(self) -> None:
        """Set _work_time_left back to _work_time.

        >>> p = PomodomoApp()
        >>> wt = _WorkTimer(p)
        >>> wt._work_time_left = datetime.timedelta(seconds = 1)
        >>> wt._work_time_left != wt._work_time
        True

        >>> wt.reset_time_left()
        >>> wt._work_time_left == wt._work_time
        True
        """
        self._work_time_left = self._work_time
        self.config(text=str(self._work_time))

    def set_work_time(self, input_time: str) -> bool:
        """Takes user-inputted work time from the work time entry box
        widget, and updates self._work_time, self._work_time_left, as well
        as the label text to reflect this new input time.

        Returns True if user-inputted time was a valid number and _WorkTime
        object was successfully updated, and False otherwise.
        >>> p = PomodomoApp()
        >>> wt = _WorkTimer(p)
        >>> wt.set_work_time('abc')  # invalid work time
        False

        # _WorkTime object not updated after invalid time passed in
        >>> wt._work_time == datetime.timedelta(minutes = 25)
        True
        >>> wt._work_time_left == wt._work_time
        True
        >>> wt['text'] == str(datetime.timedelta(minutes = 25))
        True

        >>> wt.set_work_time('30')  # valid input of 30 and a half minutes
        True

        # _WorkTime object is successfully updated after valid time passed in
        >>> wt._work_time == datetime.timedelta(minutes = 30)
        True
        >>> wt._work_time_left == wt._work_time
        True
        >>> wt['text'] == str(datetime.timedelta(minutes = 30))
        True
        """
        # Take inputted work time from an entry widget, set label to that
        # amount of time, and set _work_time and _work_time_left to that time

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
        else:
            minutes = 0

        # get seconds from user input time
        seconds = round((float(input_time) - minutes) * 60)

        new_work_time = datetime.timedelta(hours=hours, minutes=minutes,
                                           seconds=seconds)

        # Update _work_time and _work_time_left to the new user-inputted work
        # time, and change text of the _WorkTime object to reflect the new
        # work time
        self._work_time = new_work_time
        self._work_time_left = new_work_time
        self.config(text=str(new_work_time))

        # Finally, return True to indicate input time was valid and _WorkTimer
        # successfully updated
        return True

    def countdown(self) -> None:
        """Subtracts one second from _work_time_left, and updates the on-screen
        label text of the _WorkTime object to reflect the new _work_time_left.

        >>> p = PomodomoApp()
        >>> wt = _WorkTimer(p)
        >>> initial_work_time = wt._work_time
        >>> initial_work_time_left = wt._work_time_left

        >>> initial_work_time == datetime.timedelta(minutes = 25)
        True
        >>> initial_work_time_left == datetime.timedelta(minutes = 25)
        True
        >>> expected = initial_work_time - datetime.timedelta(seconds = 1)

        >>> wt.countdown()
        >>> str(wt._work_time) == str(initial_work_time)
        True
        >>> str(wt._work_time_left) == str(expected)
        True
        """
        self._work_time_left -= datetime.timedelta(seconds=1)
        self.config(text=str(self._work_time_left))


class _BreakTimer(Label):
    """A Label subclass for keeping track of how much time the user rests in
    a single Pomodoro cycle, in PomodomoApp. Also creates a label widget on the
    PomodomoApp window to show how much break time a user has left.

    === Private attributes ===
    _root: The PomodomoApp tkinter window that _BreakTimer belongs to.

    _break_time: A datetime.timedelta object indicating how long the user rests
    for, in a single Pomodoro cycle.

    _break_time_left: A datetime.timedelta object tracking how much time a user
    has left to rest, in a given Pomodoro cycle.

    === Representational invariants ===
    - _root is an instance of PomodomoApp
    - _break_time is a valid, non-zero time in datetime.timedelta
    - _break_time_left is a valid, non-zero time in datetime.timedetla
    - datetime.timedelta(seconds = 0) <= _break_time_left <= _break_time
    """
    _root: PomodomoApp
    _break_time: datetime.timedelta
    _break_time_left: datetime.timedelta

    def __init__(self, root: PomodomoApp) -> None:
        """Initializes an instance of _BreakTimer.

        >>> p = PomodomoApp()
        >>> bt = _BreakTimer(p)
        >>> bt._root == p
        True
        >>> bt._break_time == datetime.timedelta(minutes = 5)
        True
        >>> bt._break_time_left == bt._break_time
        True
        >>> bt['text'] == str(bt._break_time_left)
        True
        """
        self._root = root

        # Treat _BreakTimer as a normal Label object, setting font to size 48
        # Arial, with black font color and white background.
        Label.__init__(self, root, font=('Arial', 48), fg='black',
                       bg='white')

        # Initialize _work_time to 25 minutes, and _work_time_left to 25
        # minutes as well
        self._break_time = datetime.timedelta(minutes=5)
        self._break_time_left = self._break_time

        # Finally, set the label text of _BreakTime to _break_time_left
        self.config(text=str(self._break_time_left))

    def get_break_time(self) -> str:
        """Returns the string of self._break_time.

        >>> p = PomodomoApp()
        >>> bt = _BreakTimer(p)
        >>> bt.get_break_time()
        '0:05:00'
        """
        return str(self._break_time)

    def get_break_time_left(self) -> str:
        """Returns the string of self._work_time_left.

        >>> p = PomodomoApp()
        >>> bt = _BreakTimer(p)
        >>> bt.get_break_time_left()
        '0:05:00'
        """
        return str(self._break_time_left)

    def reset_time_left(self) -> None:
        """Set _break_time_left back to _break_time.

        >>> p = PomodomoApp()
        >>> bt = _BreakTimer(p)
        >>> bt._break_time_left = datetime.timedelta(seconds = 1)
        >>> bt._break_time_left != bt._break_time
        True

        >>> bt.reset_time_left()
        >>> bt._break_time_left == bt._break_time
        True
        """
        self._break_time_left = self._break_time
        self.config(text=str(self._break_time))

    def set_break_time(self, input_time: str) -> bool:
        """Takes user-inputted break time from the break time entry box
        widget, and updates self._break_time, self._break_time_left, as well
        as the label text to reflect this input time.

        Returns True if user-inputted time was a valid number and _BreakTime
        object was successfully updated, and False otherwise.
        >>> p = PomodomoApp()
        >>> bt = _BreakTimer(p)
        >>> bt.set_break_time('abc')  # invalid work time
        False

        # _WorkTime object not updated after invalid time passed in
        >>> bt._break_time == datetime.timedelta(minutes = 5)
        True
        >>> bt._break_time_left == bt._break_time
        True
        >>> bt['text'] == str(datetime.timedelta(minutes = 5))
        True

        >>> bt.set_break_time('10')  # valid input of 10 minutes
        True

        # _WorkTime object is successfully updated after valid time passed in
        >>> bt._break_time == datetime.timedelta(minutes = 10)
        True
        >>> bt._break_time_left == bt._break_time
        True
        >>> bt['text'] == str(datetime.timedelta(minutes = 10))
        True
        """
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
        else:
            minutes = 0

        # get seconds from user input time
        seconds = round((float(input_time) - minutes) * 60)

        new_break_time = datetime.timedelta(hours=hours, minutes=minutes,
                                            seconds=seconds)

        # Update _work_time and _work_time_left to the new user-inputted work
        # time, and change text of the _WorkTime object to reflect the new
        # work time
        self._break_time = new_break_time
        self._break_time_left = new_break_time
        self.config(text=str(new_break_time))

        # Finally, return True to indicate input time was valid and _WorkTimer
        # successfully updated
        return True

    def countdown(self) -> None:
        """Subtracts one second from _work_time_left, and updates the on-screen
        label text of the _WorkTime object to reflect the new _work_time_left.

        >>> p = PomodomoApp()
        >>> bt = _BreakTimer(p)
        >>> initial_break_time = bt._break_time
        >>> initial_break_time_left = bt._break_time_left

        >>> initial_break_time == datetime.timedelta(minutes = 5)
        True
        >>> initial_break_time_left == datetime.timedelta(minutes = 5)
        True
        >>> expected = initial_break_time - datetime.timedelta(seconds = 1)

        >>> bt.countdown()
        >>> str(bt._break_time) == str(initial_break_time)
        True
        >>> str(bt._break_time_left) == str(expected)
        True
        """
        self._break_time_left -= datetime.timedelta(seconds=1)
        self.config(text=str(self._break_time_left))


class _WorkTimeInput(Entry):
    """An Entry subclass for a widget of user input work time.
    """
    _root: PomodomoApp

    def __init__(self, root: PomodomoApp) -> None:
        self._root = root
        Entry.__init__(self, root, font='Arial')  # Set entry font text to arial
        self.insert(0, '25')  # default text in entry box is 25

    def disable_work_time_input(self) -> None:
        """Disable the _WorkTimeInput widget to prevent further user input.
        """
        self.config(state='disabled')

    def enable_work_time_input(self) -> None:
        """Re-enable user input for the _WorkTimeInput widget, after it was
        previously disabled.
        """
        self.config(state='normal')

    def get_user_input(self) -> str:
        """Returns the text currently entered in the _WorkTimeInput widget.

        >>> p = PomodomoApp()
        >>> wb = _WorkTimeInput(p)
        >>> wb.get_user_input()
        '25'
        """
        return self.get()


class _BreakTimeInput(Entry):
    """An Entry subclass for a widget of user input break time.
    """
    _root: PomodomoApp

    def __init__(self, root: PomodomoApp) -> None:
        self._root = root
        Entry.__init__(self, root, font='Arial')
        self.insert(0, '5')  # default text in entry box is 5

    def disable_break_time_input(self) -> None:
        """Disable the _BreakTimeInput widget to prevent further user input.
        """
        self.config(state='disabled')

    def enable_break_time_input(self) -> None:
        """Re-enable user input for the _WorkTimeInput widget, after it was
        previously disabled.
        """
        self.config(state='normal')

    def get_user_input(self) -> str:
        """Returns the text currently entered in the _BreakTimeInput widget.

        >>> p = PomodomoApp()
        >>> bb = _BreakTimeInput(p)
        >>> bb.get_user_input()
        '5'
        """
        return self.get()


class _StartStopButton(Button):
    """A Button subclass for a clickable button to start/stop PomodomoApp
    countdown.

    Pressing the button calls the start_or_pause_pomodomo_session method in
    PomodomoApp, causing the App to start/continue counting down work and break
    times, or to pause itself.

    === Attributes ===
    _root: The PomodomoApp tkinter window that _WorkTimer belongs to.

    === Representational invariants ===
    - _root is an instance of PomodomoApp
    """
    _root: PomodomoApp

    def __init__(self, root: PomodomoApp) -> None:
        self._root = root
        Button.__init__(self, root, text='Start / Pause', padx=10, pady=5,
                        command=root.start_or_pause_pomodomo_session,
                        bg='white')


class _ResetButton(Button):
    """A Button subclass for a clickable button to reset the work/break times
    in PomodomoApp, and halt its execution.

    Pressing the button calls the reset_pomodomo_session method in PomodomoApp,
    resetting the work and break timers to their starting times, and halting
    countdown on the timers.

    === Attributes ===
    _root: The PomodomoApp tkinter window that _WorkTimer belongs to.

    === Representational invariants ===
    - _root is an instance of PomodomoApp
    """
    _root: PomodomoApp

    def __init__(self, root: PomodomoApp) -> None:
        self._root = root
        Button.__init__(self, root, text='Reset', padx=10, pady=5,
                        command=root.reset_pomodomo_session,
                        bg='white')

    def disable_reset(self) -> None:
        """Disable the reset button widget.
        """
        self.config(state='disabled')

    def enable_reset(self) -> None:
        """Enable the reset button widget after it was disabled.
        """
        self.config(state='normal')


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
        self.work_timer = _WorkTimer(self)
        self.break_timer = _BreakTimer(self)

        # Create input fields for user to specify work time and break time
        # Default text in input fields is default work/break times
        self.work_time_input = _WorkTimeInput(self)
        self.break_time_input = _BreakTimeInput(self)

        # Create buttons to start/pause the app, and to reset the timers and
        # stop the app
        self.start_and_pause_button = _StartStopButton(self)
        self.reset_button = _ResetButton(self)
        self.reset_button.disable_reset()  # initialize button as disabled

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

            work_timer_setup = self.work_timer.set_work_time(input_work)
            break_timer_setup = self.break_timer.set_break_time(input_break)

            if work_timer_setup and break_timer_setup:
                self.started = True

                # start countdown loop, after a 1 second delay to prevent the
                # first second from counting down immediately
                self.after(1000, self._pomodomo_countdown_loop)

                # disable the entry boxes for work and break time when the
                # pomodomo app has started
                self.work_time_input.disable_work_time_input()
                self.break_time_input.disable_break_time_input()

                # enable the reset button
                self.reset_button.enable_reset()

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
        self.reset_button.disable_reset()

        self.work_time_input.enable_work_time_input()
        self.break_time_input.enable_break_time_input()

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
            if self.work_timer.get_work_time_left() != '0:00:00':
                self.work_timer.countdown()

            # Time left on _break_timer, so count down on that timer
            elif self.break_timer.get_break_time_left() != '0:00:00':
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


if __name__ == '__main__':
    pomodomo = PomodomoApp()
    pomodomo.mainloop()
