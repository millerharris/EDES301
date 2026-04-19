"""
--------------------------------------------------------------------------
Cycle Selector - PocketBeagle
--------------------------------------------------------------------------
Button 1 (P2_02): Cycle through 1, 2, 3 on the 7-segment display
Button 2 (P2_04): Select the current value
 
The selected number of cycles is stored in `selected_cycles` for use
by future code.
--------------------------------------------------------------------------
"""
import time
import os
 
# Import your existing drivers (assumed to be in the same directory)
from ht16k33 import HT16K33
from button   import Button
 
# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------
 
DISPLAY_BUS     = 1        # I2C bus number
DISPLAY_ADDR    = 0x70     # Default HT16K33 address
 
BUTTON1_PIN     = "P2_2"  # Cycle button
BUTTON2_PIN     = "P2_4"  # Select button
 
CYCLE_OPTIONS   = [1, 2, 3]
 
# ------------------------------------------------------------------------
# Main
# ------------------------------------------------------------------------
 
def main():
    # --- Hardware setup ---
    display = HT16K33(DISPLAY_BUS, DISPLAY_ADDR)
    button1 = Button(BUTTON1_PIN)   # Cycle
    button2 = Button(BUTTON2_PIN)   # Select
 
    current_index  = 0              # Points into CYCLE_OPTIONS
    selected_cycles = None          # Will hold the confirmed selection
 
    # Show the first option on startup
    display.update(CYCLE_OPTIONS[current_index])
    print("Cycle Selector ready.")
    print("  Button 1 (P2_02): cycle  |  Button 2 (P2_04): select")
    print("  Current value: {}".format(CYCLE_OPTIONS[current_index]))
 
    try:
        while selected_cycles is None:
 
            # Poll both buttons without blocking so we can react to either
            if button1.is_pressed():
                # Advance to next option, wrapping 1 -> 2 -> 3 -> 1
                current_index = (current_index + 1) % len(CYCLE_OPTIONS)
                display.update(CYCLE_OPTIONS[current_index])
                print("  Cycling to: {}".format(CYCLE_OPTIONS[current_index]))
 
                # Debounce: wait for button 1 to be released before continuing
                while button1.is_pressed():
                    time.sleep(0.05)
                time.sleep(0.05)   # Extra settling time
 
            elif button2.is_pressed():
                # Confirm the current selection
                selected_cycles = CYCLE_OPTIONS[current_index]
                print("  Selected: {} cycle(s)".format(selected_cycles))
 
                # Brief visual confirmation: blank then show selection again
                display.blank()
                time.sleep(0.2)
                display.update(selected_cycles)
 
                # Wait for button 2 to be released
                while button2.is_pressed():
                    time.sleep(0.05)
 
            else:
                time.sleep(0.05)   # Idle poll rate
 
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
 
    finally:
        button1.cleanup()
        button2.cleanup()
        display.blank()
 
    # ------------------------------------------------------------------
    # selected_cycles is now available for the rest of your program
    # ------------------------------------------------------------------
    print("Returning selected_cycles = {}".format(selected_cycles))
    return selected_cycles
 
 
# ------------------------------------------------------------------------
# Entry point
# ------------------------------------------------------------------------
 
if __name__ == "__main__":
    cycles = main()
    # TODO: pass `cycles` into your future code here
    print("Ready to run {} cycle(s).".format(cycles))