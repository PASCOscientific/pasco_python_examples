# This program requests a target temperature from the user and then monitors the reading from a Wireless
# Temperature Sensor until the target temperature is reached. It periodically announces the current temperature
# and terminates once it has announced that the target temperature has been reached.

from pasco import PASCOBLEDevice
from gtts import gTTS
import time
import miniaudio


ANNOUNCE_PERIOD_S = 15      # time between temperature announcements in s
CHECK_PERIOD_S = 2          # time between temperature measurements in s (should be < ANNOUNCE_PERIOD_S)

LANGUAGE = 'en'             # defines spoken language (keep as 'en' unless strings translated)
REGION = 'com'              # com is US variety of English

# play provided sound file, blocking subsequent code execution for the duration
def play_sound(phrase):
    tts = gTTS(phrase, lang=LANGUAGE, tld=REGION)
    file = 'msg.mp3'
    tts.save(file)

    stream = miniaudio.stream_file(file)
    stream_duration = miniaudio.get_file_info(file).duration

    with miniaudio.PlaybackDevice() as device:
        device.start(stream)
        time.sleep(stream_duration)

# Determine whether the requested target temperature has been reached
def target_reached(direction, target_temp, temp_sensor):
    if direction == 'increases':
        if temp_sensor.read_data('Temperature') >= target_temp:
            return True
    if direction == 'decreases':
        if temp_sensor.read_data('Temperature') <= target_temp:
            return True
    return False


def main():
    temp_sensor = PASCOBLEDevice()
    sensor_id = input("Enter your Wireless Temperature Sensor's six-digit ID (including hyphen): ")
    temp_sensor.connect_by_id(sensor_id)

    current_temp = temp_sensor.read_data('Temperature')
    print(f'The current temperature is {current_temp} degrees C.')

    target_temp = float(input("Enter your target temperature in degrees C: "))
    play_sound(f'The current temperature is {current_temp} and the target is {target_temp}')
    
    next_announce_time = time.time() + ANNOUNCE_PERIOD_S
    next_sensor_read_time = time.time()

    # Determine whether the target temperature is higher or lower than the initial temperature
    if (target_temp - current_temp) > 0:
        direction = 'increases'
    else:
        direction = 'decreases'

    while not target_reached(direction, target_temp, temp_sensor):     # read and announce temperatures until the target temp is reached
        if time.time() >= next_sensor_read_time:    # update the sensor reading every CHECK_PERIOD_S seconds
            current_temp = temp_sensor.read_data('Temperature')
            next_sensor_read_time = next_sensor_read_time + CHECK_PERIOD_S
        if time.time() >= next_announce_time:       # announce the reading every ANNOUNCE_PERIOD_S seconds
            play_sound(f'The temperature is currently {current_temp} degrees Celcius.')
            next_announce_time = next_announce_time + ANNOUNCE_PERIOD_S

    play_sound(f'Target temperature of {target_temp} has been reached!')

    temp_sensor.disconnect()


if __name__ == "__main__":
    main()