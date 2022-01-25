# For a selected single sensor measurement type, this program displays
# the requested number of readings with a specified sampling period.

from pasco import PASCOBLEDevice
import time

my_sensor = PASCOBLEDevice()

# scan for available sensors
print('\nScanning for available sensors.')
my_sensor.scan()
found_devices = my_sensor.scan()

# if no sensors are found, provide instructions and try one more time
if found_devices == []: 
    print('No sensors found.')
    input('Power on a compatible sensor and press Enter/Return to scan again. ')
    found_devices = my_sensor.scan()
    if found_devices == []:
        print('No sensors found. Quitting program.\n')
        quit()

# list available sensors and request sensor to connect to
print('Sensors found:')
print('\t#\tsensor name & ID')
for i, ble_device in enumerate(found_devices, start=1):
    print(f'\t{i}:\t{ble_device.name.split(">")[0]}')
selected_sensor_number = int(input('Enter the # of the sensor to connect to: '))
ble_device = found_devices[selected_sensor_number - 1]
print(f'\nConnecting to {ble_device.name.split(">")[0]}.')
my_sensor.connect(ble_device)
print('Connected.')

# determine sensor measurement
sensor_measurements = my_sensor.get_measurement_list()
if len(sensor_measurements) > 1:    # request desired measurement if sensors offers multiple measurements
    print('\nAvailable measurements:')
    for i, meas in enumerate(sensor_measurements, start=1):
        print(f'\t{i}:\t{meas}')
    selected_measurement_number = int(input('Select a measurement: '))
    selected_measurement = sensor_measurements[selected_measurement_number - 1]
else:                               # automatically select the measurement if sensor offers only one
    selected_measurement = sensor_measurements[0]

# request sampling parameters
samples_to_collect = int(input(f'\nHow many {selected_measurement} readings would you like to collect? '))
if samples_to_collect > 1:
    sample_period = float(input(f'How many seconds do you want between readings? '))

# display requested readings
print('\nSampling started.\n')
units = my_sensor.get_measurement_unit(selected_measurement)
for sample in range(samples_to_collect):
    reading = my_sensor.read_data(selected_measurement)
    print(f'\t{reading} {units}')
    if sample < (samples_to_collect - 1):
        time.sleep(sample_period)
print('\nSampling complete.\n')

my_sensor.disconnect()