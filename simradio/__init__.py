#!/usr/bin/python
#coding:utf-8
# Author:  Dan-Erik Lindberg -- <simradio@dan-erik.com>
# Created: 2012-07-12
# License: GPL-3

# This package contains the SimradIO application.
# SimradIO is used to view and process SIMRAD EK60 data.


# First, and before importing any Enthought packages, set the ETS_TOOLKIT
# environment variable to qt4, to tell Traits that we will use Qt.
import os
os.environ["ETS_TOOLKIT"] = "qt4"
# Having PySide installed generates an error with the QToolbar or something.
# Using only PyQt4 generates an error with sip already being set to 1 when
# you have to set it to 2 (to use str instead of QString).
# Therefore, we use pyface.qt versions of Qt classes.
from pyface.qt import QtCore, QtGui

# The simradio.py contains the main window classes.
import simradio

#----------------------------------------------------------------------
def main():
    # Don't create a new QApplication, it would unhook the Events
    # set by Traits on the existing QApplication. Simply use the
    # '.instance()' method to retrieve the existing one.
    app = QtGui.QApplication.instance()
    app.setApplicationName("SimradIO")
    window = simradio.Window()
    window.show()

    # Start the main event loop.
    app.exec_()