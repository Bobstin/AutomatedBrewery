#!/usr/bin/python

from Adafruit_I2C import Adafruit_I2C
from MCP23017 import MCP23017

import time

mcp = MCP23017(address = 0x21, num_gpios = 16) # MCP23017
outpin=0

while (outpin<16):
	print(outpin)
	mcp.pinMode(outpin, mcp.OUTPUT)
	mcp.output(outpin, 1)  # Pin High
	time.sleep(1)
	outpin +=1

outpin=0

while (outpin<16):
	print(outpin)
	mcp.pinMode(outpin, mcp.OUTPUT)
	mcp.output(outpin, 0)  # Pin Low
	time.sleep(1)
	outpin +=1
