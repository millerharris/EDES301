# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------
Cycle Selector - PocketBeagle
--------------------------------------------------------------------------
Button 1 (P2_2): Cycle through 1, 2, 3 on the 7-segment display
Button 2 (P2_4): Select the current value / Abort during countdown

Display layout during countdown:
  Digit 0 (far left) : cycles remaining
  Digit 1            : minutes (5 down to 0)
  Digit 2 & 3        : seconds (59 down to 00)
  Colon              : on between minutes and seconds

Example: 3 cycles selected, first cycle -> displays "3 5:00"
--------------------------------------------------------------------------
"""
import time
import os
import Adafruit_BBIO.GPIO as GPIO

from ht16k33 import HT16K33
from button   import Button

# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------

DISPLAY_BUS         = 1
DISPLAY_ADDR        = 0x70

BUTTON1_PIN         = "P2_2"
BUTTON2_PIN         = "P2_4"

CYCLE_OPTIONS       = [1, 2, 3]
CYCLE_DURATION_SECS = 5 * 60      # 5 minutes in seconds

# ------------------------------------------------------------------------
# Configure pins
# ------------------------------------------------------------------------

os.system("config-pin P2_2 gpio")
os.system("config-pin P2_4 gpio")

os.system("config-pin P1_36 gpio")
os.system("config-pin P1_33 gpio")
os.system("config-pin P1_31 gpio")

os.system("config-pin P1_32 gpio")
os.system("config-pin P1_30 gpio")
os.system("config-pin P1_28 gpio")

# ------------------------------------------------------------------------
# Motor setup
# ------------------------------------------------------------------------

GPIO.setup("P1_36", GPIO.OUT)   # Motor 1 STEP
GPIO.setup("P1_33", GPIO.OUT)   # Motor 1 DIR
GPIO.setup("P1_31", GPIO.OUT)   # Motor 1 SLEEP

GPIO.setup("P1_32", GPIO.OUT)   # Motor 3 STEP
GPIO.setup("P1_30", GPIO.OUT)   # Motor 3 DIR
GPIO.setup("P1_28", GPIO.OUT)   # Motor 3 SLEEP

# ------------------------------------------------------------------------
# Motor functions
# ------------------------------------------------------------------------

def run_motor1(button2):
    """Run Motor 1 before each cycle."""
    print("  Running Motor 1...")

    GPIO.output("P1_31", GPIO.HIGH)   # Wake up
    time.sleep(0.01)

    # Change GPIO.HIGH to GPIO.LOW to reverse Motor 1 direction
    GPIO.output("P1_33", GPIO.HIGH)

    for i in range(100):            # TODO: change 10000 to adjust Motor 1 steps
        if button2.is_pressed():
            GPIO.output("P1_31", GPIO.LOW)
            print("  Aborted during Motor 1!")
            return False
        GPIO.output("P1_36", GPIO.HIGH)
        time.sleep(0.005)             # TODO: change 0.005 to adjust Motor 1 speed
        GPIO.output("P1_36", GPIO.LOW)
        time.sleep(0.005)

    GPIO.output("P1_31", GPIO.LOW)    # Sleep
    print("  Motor 1 done.")
    return True

# End def


def run_motor3(button2):
    """Run Motor 3 after each cycle."""
    print("  Running Motor 3...")

    GPIO.output("P1_28", GPIO.HIGH)   # Wake up
    time.sleep(0.01)

    # Change GPIO.LOW to GPIO.HIGH to reverse Motor 3 direction
    GPIO.output("P1_30", GPIO.LOW)

    for i in range(100):             # TODO: change 1000 to adjust Motor 3 steps
        if button2.is_pressed():
            GPIO.output("P1_31", GPIO.LOW)
            print("  Aborted during Motor 1!")
            return False
        GPIO.output("P1_32", GPIO.HIGH)
        time.sleep(0.01)              # TODO: change 0.01 to adjust Motor 3 speed
        GPIO.output("P1_32", GPIO.LOW)
        time.sleep(0.01)

    GPIO.output("P1_28", GPIO.LOW)    # Sleep
    print("  Motor 3 done.")
    return True

# End def

# ------------------------------------------------------------------------
# Countdown function
# ------------------------------------------------------------------------

def run_countdown(display, cycles_remaining, button2):
    """Count down 5 minutes, showing cycles left on far left digit.

    Returns True if completed normally, False if aborted by button 2.
    """

    print("  Starting countdown: {} cycle(s) remaining".format(cycles_remaining))

    for seconds_left in range(CYCLE_DURATION_SECS, -1, -1):

        # Check for abort press
        if button2.is_pressed():
            print("\n  Aborted by user!")
            return False       # False = aborted

        mins = seconds_left // 60
        secs = seconds_left % 60

        # Update each digit individually
        display.set_digit(0, cycles_remaining)   # Far left: cycles left
        display.set_digit(1, mins)               # Minutes
        display.set_digit(2, secs // 10)         # Tens of seconds
        display.set_digit(3, secs % 10)          # Units of seconds
        display.set_colon(True)                  # Colon between mins and secs

        time.sleep(1)

    print("  Cycle complete.")
    return True                # True = finished normally

# End def

# ------------------------------------------------------------------------
# Selection loop
# ------------------------------------------------------------------------

def select_cycles(display, button1, button2):
    """Use buttons to select number of cycles. Returns selected value."""
    current_index = 0
    display.update(CYCLE_OPTIONS[current_index])
    print("Select number of cycles:")
    print("  Button 1 (P2_2): cycle  |  Button 2 (P2_4): select")
    print("  Current value: {}".format(CYCLE_OPTIONS[current_index]))

    while True:
        if button1.is_pressed():
            current_index = (current_index + 1) % len(CYCLE_OPTIONS)
            display.update(CYCLE_OPTIONS[current_index])
            print("  Cycling to: {}".format(CYCLE_OPTIONS[current_index]))

            while button1.is_pressed():
                time.sleep(0.05)
            time.sleep(0.05)

        elif button2.is_pressed():
            selected = CYCLE_OPTIONS[current_index]
            print("  Selected: {} cycle(s)".format(selected))

            # Blink confirmation
            display.blank()
            time.sleep(0.2)
            display.update(selected)

            while button2.is_pressed():
                time.sleep(0.05)

            return selected

        else:
            time.sleep(0.05)

# End def

# ------------------------------------------------------------------------
# Main
# ------------------------------------------------------------------------

def main():
    display = HT16K33(DISPLAY_BUS, DISPLAY_ADDR)
    button1 = Button(BUTTON1_PIN)
    button2 = Button(BUTTON2_PIN)

    try:
        # Step 1: Select number of cycles
        selected_cycles = select_cycles(display, button1, button2)

        # Step 2: Run each cycle with a 5 minute countdown
        print("\nStarting {} cycle(s)...\n".format(selected_cycles))

        for i in range(selected_cycles):
            cycles_remaining = selected_cycles - i

            # --- Pre-cycle: Motor 1 ---
            if not run_motor1(button2):
                print("\nCycles aborted!")
                break

            # --- Countdown timer ---
            completed = run_countdown(display, cycles_remaining, button2)

            if not completed:
                print("\nCycles aborted!")
                break

            # --- Post-cycle: Motor 3 ---
            if not run_motor3(button2):
                print("\nCycles aborted!")
                break

        # Step 3: Done
        print("\nAll cycles complete!")
        display.set_colon(False)
        display.blank()

    except KeyboardInterrupt:
        print("\nStopped by user.")

    finally:
        button1.cleanup()
        button2.cleanup()
        display.set_colon(False)
        display.blank()
        GPIO.cleanup()
# ------------------------------------------------------------------------
# Entry point
# ------------------------------------------------------------------------

if __name__ == "__main__":
    main()
