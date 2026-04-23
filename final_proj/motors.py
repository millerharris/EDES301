# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------
Motor Test - A4988 + 28BYJ-48
--------------------------------------------------------------------------
Just runs the motor a small amount when the script is executed.
No buttons needed - just hit run.

Pins:
  STEP   -> P1_36
  DIR    -> P1_33
  SLEEP  -> P1_31  (or tied to 3.3V)
  RESET  -> tied to SLEEP
  ENABLE -> tied to GND (always enabled)
  MS1    -> 3.3V  ]
  MS2    -> GND   ] Half step mode
  MS3    -> GND   ]
--------------------------------------------------------------------------
"""
import time
import os
import Adafruit_BBIO.GPIO as GPIO

# ------------------------------------------------------------------------
# Configure pins
# ------------------------------------------------------------------------

os.system("config-pin P1_36 gpio")
os.system("config-pin P1_33 gpio")
os.system("config-pin P1_31 gpio")

# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------

STEP_PIN    = "P1_36"
DIR_PIN     = "P1_33"
SLEEP_PIN   = "P1_31"

STEP_DELAY  = 0.005     # seconds between steps (lower = faster)
NUM_STEPS   = 10000       # number of steps to take

# ------------------------------------------------------------------------
# Setup
# ------------------------------------------------------------------------

GPIO.setup(STEP_PIN,  GPIO.OUT)
GPIO.setup(DIR_PIN,   GPIO.OUT)
GPIO.setup(SLEEP_PIN, GPIO.OUT)

# Wake up the driver
GPIO.output(SLEEP_PIN, GPIO.HIGH)
time.sleep(0.01)   # Give driver a moment to wake up

# Set direction (change to GPIO.LOW to reverse)
GPIO.output(DIR_PIN, GPIO.HIGH)

# ------------------------------------------------------------------------
# Move the motor
# ------------------------------------------------------------------------

print("Motor test starting...")
print("Taking {} steps...".format(NUM_STEPS))

for i in range(NUM_STEPS):
    GPIO.output(STEP_PIN, GPIO.HIGH)
    time.sleep(STEP_DELAY)
    GPIO.output(STEP_PIN, GPIO.LOW)
    time.sleep(STEP_DELAY)

print("Done!")

# Put driver to sleep to save power
GPIO.output(SLEEP_PIN, GPIO.LOW)

# Cleanup
GPIO.cleanup()