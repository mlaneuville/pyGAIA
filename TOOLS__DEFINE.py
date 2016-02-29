#!/usr/bin/python

from struct import unpack

def read_int(f):
	byte = f.read(4)
	n = unpack('<L', byte)  # little endian
	t = int(n[0])
	return t

def read_db(f):
	byte = f.read(8)
	n = unpack('<d', byte)  # little endian
	t = float(n[0])
	return t
