#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : Jason Jiang
# Created Date: August 16, 2021
# Last Updated: August 22, 2021
# version = 0.0
# ---------------------------------------------------------------------------

"""This module provides the classes for user entry boxes in PomodomoApp, to
set their own work and break times."""

# ---------------------------------------------------------------------------

import tkinter as tk
# Imports
from tkinter import Entry


class _UserTimeInput(Entry):
    """An Entry subclass to allow users to input work and break times, in the
    Pomo-do-mo app.
    """

    def __init__(self, root: tk.Tk) -> None:
        Entry.__init__(self, root, font='Arial')

    def disable_input(self) -> None:
        """Disable the _UserTimeInput widget to prevent further user input.
        """
        self.config(state='disabled')

    def enable_input(self) -> None:
        """Re-enable user input for the _UserTimeInput widget, after it was
        previously disabled.
        """
        self.config(state='normal')

    def get_user_input(self) -> str:
        """Returns the text currently entered in the _UserTimeInput widget.
        '25'
        """
        return self.get()


class _WorkTimeInput(_UserTimeInput):
    """An _UserTimeInput subclass for a widget of user input work time.
    """

    def __init__(self, root: tk.Tk) -> None:
        _UserTimeInput.__init__(self, root)

        # Have 25 minutes inputted in user work time widget by default
        self.insert(0, '25')


class _BreakTimeInput(_UserTimeInput):
    """An _UserTimeInput subclass for a widget of user input break time.
    """

    def __init__(self, root: tk.Tk) -> None:
        _UserTimeInput.__init__(self, root)

        # Have 5 minutes inputted in user break time widget by default
        self.insert(0, '5')
