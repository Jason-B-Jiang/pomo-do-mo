#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : Jason Jiang
# Created Date: August 16, 2021
# Last updated: August 22, 2021
# version = 0.1
# ---------------------------------------------------------------------------

"""This module provides a class for creating consistent button widgets, in the
Pomo-do-mo Tkinter app.
"""

# ---------------------------------------------------------------------------

# Imports
import tkinter as tk
from tkinter import Button
from typing import Callable


class _Button(Button):
    """A class for creating similarly formatted buttons in the Pomodomo
    Tkinter application.

    Each button in the Pomodomo Tkinter app should have similar sizes and
    appearences, but will have different button texts and button functions.
    """

    def __init__(self, root: tk.Tk, text: str, button_command: Callable):
        """Create a generic button of a fixed size and white background.
        """
        Button.__init__(self, root, text=text, padx=10, pady=5,
                        command=button_command,
                        bg='white')

    def disable_button(self) -> None:
        """Disable the button widget.
        """
        self.config(state='disabled')

    def enable_button(self) -> None:
        """Enable the button widget.
        """
        self.config(state='normal')
