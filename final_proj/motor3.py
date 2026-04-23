# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------
Motor 2 Test - A4988 + 12V Stepper
--------------------------------------------------------------------------
Pins:
  STEP   -> P1_32
  DIR    -> P1_30
  SLEEP  -> P1_28
  ENABLE -> GND (hardwired)
  MS1    -> 3.3V (half step)
  MS2    -> GND
  MS3    -> GND
--------------------------------------------------------------------------
"""
import time
import os
import Adafruit_BBIO.GPIO as GPIO

# ------------------------------------------------------------------------
# Configure pins
# ------------------------------------------------------------------------

os.system("config-pin P1_32 gpio")
os.system("config-pin P1_30 gpio")
os.system("config-pin P1_28 gpio")

# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------

STEP_PIN    = "P1_32"
DIR_PIN     = "P1_30"
SLEEP_PIN   = "P1_28"

STEP_DELAY  = 0.01     # seconds between steps (lower = faster)
NUM_STEPS   = 1000 # number of steps to take

# ------------------------------------------------------------------------
# Setup
# ------------------------------------------------------------------------

GPIO.setup(STEP_PIN,  GPIO.OUT)
GPIO.setup(DIR_PIN,   GPIO.OUT)
GPIO.setup(SLEEP_PIN, GPIO.OUT)

# Wake up the driver
GPIO.output(SLEEP_PIN, GPIO.HIGH)
time.sleep(0.01)

# Set direction (change to GPIO.LOW to reverse)
GPIO.output(DIR_PIN, GPIO.LOW)

# ------------------------------------------------------------------------
# Move the motor
# ------------------------------------------------------------------------

print("Motor 2 test starting...")
print("Taking {} steps...".format(NUM_STEPS))

for i in range(NUM_STEPS):
    GPIO.output(STEP_PIN, GPIO.HIGH)
    time.sleep(STEP_DELAY)
    GPIO.output(STEP_PIN, GPIO.LOW)
    time.sleep(STEP_DELAY)

print("Done!")

# Put driver to sleep
GPIO.output(SLEEP_PIN, GPIO.LOW)

# Cleanup
GPIO.cleanup()
