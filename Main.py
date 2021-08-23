#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Created By  : Jason Jiang
# Created Date: August 22, 2021
# version = 0.0
# ---------------------------------------------------------------------------

"""This module runs the PomodomoApp Tkinter application."""

# TODO:
#
# 1) Create a pop up window for a brief tutorial on how to use the Pomo-do-mo
#    app
#
# 2) Keep track of how many Pomodoro cycles a user has worked through in a
#    single session of using the app, and how much time they've worked
#
# 3) Create a pop-up window telling users to input valid number of minutes into
#    the entry boxes, when an invalid input is given
#
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    from PomodomoApp import *
    pomodomo = PomodomoApp()
    pomodomo.mainloop()
