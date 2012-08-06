#!/usr/bin/python
#coding:utf-8
# Author:  Dan-Erik Lindberg -- <simradio@dan-erik.com>
# Created: 2012-07-12
# License: GPL-3

import os
import sys

import distutils

distutils.core.setup(
    name='simradio',
    version='12.10',
    license='GPL-3',
    author='Dan-Erik Lindberg',
    author_email='simradio@dan-erik.com',
    keywords=["SIMRAD","sonar","echo sounder","echo","bathymetry","fish finder"],
    description='SimradIO stores and processes data from a SIMRAD EK60 echo sounder.',
    long_description = """\
SimradIO
-------------------------------------

Works with data from the SIMRAD EK60 scientific echo sounder. Our test hardware
is the EK60 with one or two 7C split beam transducers.
""",
    classifiers = [
           "Programming Language :: Python",
           #"Programming Language :: Python :: 3",
           "Operating System :: Windows",
           "Operating System :: Linux",
           "Operating System :: OS Independent"
           ],
    url='https://github.com/GaRyu/simradio'
    )

