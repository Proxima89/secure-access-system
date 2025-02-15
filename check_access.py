import smbus
import time
from db_connect import db_connection
from gpiozero import Buzzer
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import mysql.connector
from datetime import datetime
import os
import sys
import warnings

# Suppress gpiozero warnings
warnings.filterwarnings("ignore", category=UserWarning, module="gpiozero")

# Define I2C device address
LCD_ADDR = 0x27

# Define some constants for the LCD
LCD_WIDTH = 16  # Maximum characters per line
LCD_CHR = 1  # Mode - Sending data
LCD_CMD = 0  # Mode - Sending command
LCD_LINE_1 = 0x80  # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0  # LCD RAM address for the 2nd line
LCD_CLEAR = 0x01  # Clear LCD command
LCD_BACKLIGHT = 0x08  # On
ENABLE = 0b00000100  # Enable bit

# Set up GPIO for relay control
RELAY_PIN = 18  # GPIO18 (pin 12)
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)
GPIO.output(RELAY_PIN, 0)
# GPIO.output(RELAY_PIN, GPIO.LOW)  # Start with the relay off

def lcd_init():
  # Initialize the display
  lcd_byte(0x33, LCD_CMD)
  lcd_byte(0x32, LCD_CMD)
  lcd_byte(0x06, LCD_CMD)
  lcd_byte(0x0C, LCD_CMD)
  lcd_byte(0x28, LCD_CMD)
  lcd_byte(LCD_CLEAR, LCD_CMD)
  time.sleep(0.05)

def lcd_byte(bits, mode):
  # Send byte to data pins
  bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
  bits_low = mode | ((bits << 4) & 0xF0) | LCD_BACKLIGHT

  # High bits
  bus.write_byte(LCD_ADDR, bits_high)
  lcd_toggle_enable(bits_high)

  # Low bits
  bus.write_byte(LCD_ADDR, bits_low)
  lcd_toggle_enable(bits_low)

def lcd_toggle_enable(bits):
  # Toggle enable
  time.sleep(0.0005)
  bus.write_byte(LCD_ADDR, (bits | ENABLE))
  time.sleep(0.0005)
  bus.write_byte(LCD_ADDR, (bits & ~ENABLE))
  time.sleep(0.0005)

def lcd_string(message):
  # Send string to display
  message = message.ljust(LCD_WIDTH, " ")
  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]), LCD_CHR)

def execute_query(query, params=None):
  try:
    db = db_connection()
    cursor = db.cursor()
    cursor.execute(query, params)
    result = cursor.fetchall()
    db.commit()
    db.close()
    return result
  except mysql.connector.Error as err:
    print(f"Error: {err}")
    return None

def main():
  # Open I2C interface
  global bus
  bus = smbus.SMBus(1)

  # Initialize the LCD
  lcd_init()

  reader = SimpleMFRC522()
  buzzer = Buzzer(26)

  lcd_byte(LCD_LINE_1, LCD_CMD)
  lcd_string("Tap your card")
  lcd_byte(LCD_LINE_2, LCD_CMD)
  lcd_string("")

  try:
    while True:
      print("Reading RFID...")

      id, text = reader.read()
      query = "SELECT id, name FROM users WHERE rfid_uid=%s"
      result = execute_query(query, (str(id),))

      if result and len(result) >= 1:
        user_id = result[0][0]
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # Check if the user already has a clock_in entry with no clock_out
        query = "SELECT id FROM attendance WHERE user_id = %s AND clock_out IS NULL"
        existing_entry = execute_query(query, (user_id,))

        if existing_entry and len(existing_entry) >= 1:
          # Update the existing entry with the current timestamp for clock_out
          query = "UPDATE attendance SET clock_out = %s WHERE id = %s"
          execute_query(query, (current_time, existing_entry[0][0]))
          print("User signed out.")
          lcd_byte(LCD_LINE_1, LCD_CMD)
          lcd_string("User: " + result[0][1].strip())
          lcd_byte(LCD_LINE_2, LCD_CMD)
          lcd_string("Signed out")
          buzzer.on()
          time.sleep(0.75)
          buzzer.off()

          # Open the relay (send HIGH signal)
          GPIO.output(RELAY_PIN, 1)
          time.sleep(2)  # Keep relay on for 3 seconds
          GPIO.output(RELAY_PIN, 0)

          time.sleep(3)
          lcd_byte(LCD_LINE_1, LCD_CMD)
          lcd_string("Tap your card")
          lcd_byte(LCD_LINE_2, LCD_CMD)
          lcd_string("")

          # Restart the application
          print("Restarting application...")
          GPIO.cleanup()
          os.execv(sys.executable, ["python"] + sys.argv)
        else:
          # This is a clock in action
          query = "INSERT INTO attendance (user_id, clock_in, clock_out) VALUES (%s, %s, NULL)"
          execute_query(query, (user_id, current_time))
          print("User signed in.")
          lcd_byte(LCD_LINE_1, LCD_CMD)
          lcd_string("User: " + result[0][1].strip())
          lcd_byte(LCD_LINE_2, LCD_CMD)
          lcd_string("Signed in")
          buzzer.on()
          time.sleep(0.5)
          buzzer.off()

          # Open the relay (send HIGH signal)
          GPIO.output(RELAY_PIN, 1)
          time.sleep(2)  # Keep relay on for 3 seconds
          GPIO.output(RELAY_PIN, 0)

          time.sleep(3)
          lcd_byte(LCD_LINE_1, LCD_CMD)
          lcd_string("Tap your card")
          lcd_byte(LCD_LINE_2, LCD_CMD)
          lcd_string("")

          # Restart the application
          print("Restarting application...")
          GPIO.cleanup()
          os.execv(sys.executable, ["python"] + sys.argv)

        time.sleep(3)
      else:
        print("User not found.")
        time.sleep(2)
  finally:
    print("Process terminated.")
    GPIO.cleanup()

if __name__ == "__main__":
  main()
