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
            completed = run_countdown(display, cycles_remaining, button2)
 
            if not completed:
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
 
# ------------------------------------------------------------------------
# Entry point
# ------------------------------------------------------------------------
 
if __name__ == "__main__":
    main()