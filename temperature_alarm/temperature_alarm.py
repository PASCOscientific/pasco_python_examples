# This program requests a target temperature from the user and then monitors the reading from a Wireless
# Temperature Sensor until the target temperature is reached. It periodically announces the current temperature
# and terminates once it has announced that the target temperature has been reached.

from pasco import PASCOBLEDevice
from gtts import gTTS
import time
import miniaudio

# play provided sound file, blocking subsequent code execution for the duration
def play_sound(file):
    stream = miniaudio.stream_file(file)
    stream_duration = miniaudio.get_file_info(file).duration
    with miniaudio.PlaybackDevice() as device:
        device.start(stream)
        time.sleep(stream_duration)

# Determine whether the requested target temperature has been reached
def target_reached():   # True once target temp has been reached or passed in appropriate direction
    if direction == 'increases':
        if temp_sensor.read_data('Temperature') >= target_temp:
            return True
    if direction == 'decreases':
        if temp_sensor.read_data('Temperature') <= target_temp:
            return True
    return False

ANNOUNCE_PERIOD_S = 15      # time between temperature announcements in s
CHECK_PERIOD_S = 2          # time between temperature measurements in s (should be < ANNOUNCE_PERIOD_S)

LANGUAGE = 'en'             # defines spoken language (keep as 'en') unless strings translated
REGION = 'com'           # defines the accent of English spoken ('com'=US, 'co.uk'=UK, 'com.au'=AUS, 'co.in'=IN)

temp_sensor = PASCOBLEDevice()

print("This program will inform you when the temperature sensor reading reaches a specified value.")
print("Turn on your sensor and your computer speakers to hear the spoken notifications.")
sensor_id = input("Enter your Wireless Temperature Sensor's six-digit ID (including hyphen): ")

print("Connecting to sensor...")
temp_sensor.connect_by_id(sensor_id)
print("Connected.")

initial_temp = temp_sensor.read_data('Temperature')
print(f'The current temperature is {initial_temp} degrees C.')

target_temp = float(input("Enter your target temperature in degrees C: "))

# Determine whether the target temperature is higher or lower than the initial temperature
if (target_temp - initial_temp) > 0:
    direction = 'increases'
else:
    direction = 'decreases'

tts = gTTS(f'The temperature is currently {initial_temp} degrees Celcius.'
           f' I will monitor it and let you know when it {direction} to {target_temp}.', lang=LANGUAGE, tld=REGION)
next_announce_time = time.time() + ANNOUNCE_PERIOD_S
tts.save('msg.mp3')
play_sound('msg.mp3')

current_temp = temp_sensor.read_data('Temperature')
next_sensor_read_time = time.time() + CHECK_PERIOD_S

while not target_reached():     # read and announce temperatures until the target temp is reached
    if time.time() >= next_sensor_read_time:    # update the sensor reading every CHECK_PERIOD_S seconds
        current_temp = temp_sensor.read_data('Temperature')
        next_sensor_read_time = next_sensor_read_time + CHECK_PERIOD_S
    if time.time() >= next_announce_time:       # announce the reading every ANNOUNCE_PERIOD_S seconds
        tts = gTTS(f'The temperature is currently {current_temp} degrees Celcius.', lang=LANGUAGE, tld=REGION)
        tts.save('msg.mp3')
        play_sound('msg.mp3')
        next_announce_time = next_announce_time + ANNOUNCE_PERIOD_S

# target temperature has been reached
tts = gTTS(f'Woohoo! Your target temperature of {target_temp} has been reached. Goodbye.', lang=LANGUAGE, tld=REGION)
tts.save('msg.mp3')
play_sound('msg.mp3')

temp_sensor.disconnect()