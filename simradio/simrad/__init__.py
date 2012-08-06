#!/usr/bin/python
#coding:utf-8
# Author:  Dan-Erik Lindberg -- <simradio@dan-erik.com>
# Created: 2012-07-12
# License: GPL-3

# This package contains general classes to deal with SIMRAD hardware
# or dealing with importing/exporting SIMRAD data from specific
# software vendors.

# A lot of the functionality was "stolen" from the Matlab package 
# maintained by Rick Towler at NOAA Alaska Fisheries Science Center.

import os
import struct
import datetime as dt

# Constants

HEADER_LEN = 12                              # Bytes in datagram header
DATA_LEN = 2500                              # Bytes in data chunks

########################################################################
class ek60():
	""""""

	#----------------------------------------------------------------------
	def __init__(self):
		"""Constructor"""

	#----------------------------------------------------------------------
	def read_fileheader(self, filename):
		"""read_fileheader(filename) returns the raw file header data in a dictionary:
		- header["dgType"]
		Datagram type, e.g. "CON0"
		- header["datetime"]
		Date/time in epoch format (since 1970)
		- header["datetext"]
		Date/time in string format
		- header["surveyname"]
		- header["transectname"]
		- header["soundername"]
		- header["transceivercount"]
		- header["transceiverconfigs"]
		Another dictionary consisting of configuaration parameters for each transceiver:
			transceiverconfigs[t]["channelid"]
			transceiverconfigs[t]["beamtype"]
			transceiverconfigs[t]["frequency"]
			transceiverconfigs[t]["gain"]
			transceiverconfigs[t]["equivalentbeamangle"]
			transceiverconfigs[t]["beamwidthalongship"]
			transceiverconfigs[t]["beamwidthathwartship"]
			transceiverconfigs[t]["anglesensitivityalongship"]
			transceiverconfigs[t]["anglesensitivityathwartship"]
			transceiverconfigs[t]["angleoffsetalongship"]
			transceiverconfigs[t]["angleoffsetathwartship"]
			transceiverconfigs[t]["posx"]
			transceiverconfigs[t]["posy"]
			transceiverconfigs[t]["posz"]
			transceiverconfigs[t]["dirx"]
			transceiverconfigs[t]["diry"]
			transceiverconfigs[t]["dirz"]
			transceiverconfigs[t]["pulselengthtable"]
			transceiverconfigs[t]["spare2"]
			transceiverconfigs[t]["gaintable"]
			transceiverconfigs[t]["spare3"]
			transceiverconfigs[t]["sacorrectiontable"]
			transceiverconfigs[t]["spare4"]
		- header["headerlength"]
		Use header length to decide where to begin reading data samples with read_filedata()."""
		# Just make sure the filename is actually valid
		if os.path.exists(filename):
			f = open(filename, "rb")
			# First byte is the length of the header. 
			# This should be 848 for one transducer, and longer for several transducers.
			headerlength = int(struct.unpack("<i", f.read(4))[0])
			# Datagram Header
			# DG type = "CON0"
			dgType = "".join(struct.unpack("<4c", f.read(4)))
			# Time is stored as a 64-bit number
			# Time is nanoseconds passed since 1601, so we will forward this
			# to 1970 epoch used by Posix systems. To ensure 32-bit compatibility
			# we read the 64-bit number in two 32-bit and then add them up.
			lowdatetime = struct.unpack("<L", f.read(4))[0]
			highdatetime = struct.unpack("<L", f.read(4))[0]
			datetime = (float(highdatetime) * 2**32 + lowdatetime) * 1e-7 - 11644473600
			# Configuration
			surveyname = "".join(struct.unpack("<128c", f.read(128))).rstrip("\x00")
			transectname = "".join(struct.unpack("<128c", f.read(128))).rstrip("\x00")
			soundername = "".join(struct.unpack("<128c", f.read(128))).rstrip("\x00")
			spare = "".join(struct.unpack("<128c", f.read(128))).rstrip("\x00")         # Says "2.2.0" in my test data file
			transceivercount = struct.unpack("<i", f.read(4))[0]
			# Transceiver configurations
			transceiverconfigs = {}
			for t in range(transceivercount):
				transceiverconfigs[t] = {"channelid":"".join(struct.unpack("<128c", f.read(128))).rstrip("\x00"), 
				                         "beamtype":struct.unpack("<i", f.read(4))[0], 
				                         "frequency":struct.unpack("<f", f.read(4))[0],
				                         "gain":struct.unpack("<f", f.read(4))[0],
				                         "equivalentbeamangle":struct.unpack("<f", f.read(4))[0],
				                         "beamwidthalongship":struct.unpack("<f", f.read(4))[0],
				                         "beamwidthathwartship":struct.unpack("<f", f.read(4))[0],
				                         "anglesensitivityalongship":struct.unpack("<f", f.read(4))[0],
				                         "anglesensitivityathwartship":struct.unpack("<f", f.read(4))[0],
				                         "angleoffsetalongship":struct.unpack("<f", f.read(4))[0],
				                         "angleoffsetathwartship":struct.unpack("<f", f.read(4))[0],
				                         "posx":struct.unpack("<f", f.read(4))[0],
				                         "posy":struct.unpack("<f", f.read(4))[0],
				                         "posz":struct.unpack("<f", f.read(4))[0],
				                         "dirx":struct.unpack("<f", f.read(4))[0],
				                         "diry":struct.unpack("<f", f.read(4))[0],
				                         "dirz":struct.unpack("<f", f.read(4))[0],
				                         "pulselengthtable":struct.unpack("<5f", f.read(20)),
				                         "spare2":"".join(struct.unpack("<8c", f.read(8))).rstrip("\x00"),
				                         "gaintable":struct.unpack("<5f", f.read(20)),
				                         "spare3":"".join(struct.unpack("<8c", f.read(8))).rstrip("\x00"),
				                         "sacorrectiontable":struct.unpack("<5f", f.read(20)),
				                         "spare4":"".join(struct.unpack("<52c", f.read(52))).replace("\x00",''),}
			header = {"dgType":dgType, 
		                  "datetime":datetime,
			          "datetext":str(dt.datetime.fromtimestamp(datetime)),
		                  "surveyname":surveyname,
		                  "transectname":transectname,
		                  "soundername":soundername,
		                  "transceivercount":transceivercount,
			          "transceiverconfigs":transceiverconfigs,
			          "headerlength":headerlength}
			f.close()
			return header

	#----------------------------------------------------------------------
	def read_filedata(self, filename, startbyte=848):
		"""read_filedata(filename, startbyte)
		Filname is the name of a .raw data file created with e.g. ER60 software.
		Startbyte should be header length, which you get from read_fileheader()."""
		# Just make sure the filename is actually valid
		if os.path.exists(filename):
			f = open(filename, "rb")
			# We will just read X bytes to skip the header. This data is junk, because we already read it
			# with the read_fileheader() function.
			junk = f.read(startbyte)