#!/usr/bin/python
#coding:utf-8
# Author:  Dan-Erik Lindberg -- <simradio@dan-erik.com>
# Created: 2012-07-12
# License: GPL-3

# This is the "binary" file that will start the application

import gettext
from gettext import gettext as _
gettext.textdomain('simradio')

import simradio
simradio.main()
