# This program plots a Smart Cart's position, velocity, and time in 
# a 3D graph at as close a sample rate as possible to the user's
# requested sample rate (computer-dependent). 
#
# Requires matplotlib 3.1.0+.

from pasco import PASCOBLEDevice
import matplotlib.pyplot as plt
import time

my_cart = PASCOBLEDevice()

# function for plotting provided 3 lists in 3 dimension graph
def plot_graph(x, y, z):
    ax.plot(x, y, z, color='b')
    ax.set_title('3D plot of Smart Cart measurements')
    ax.set_xlabel('Position (m)')
    ax.set_ylabel('Velocity (m/s)')
    ax.set_zlabel('Time (s)')
    plt.pause(0.001)

# initialize the pyplot figure
fig = plt.figure()
ax = fig.add_subplot(projection='3d')

# create lists for the time and measurements
sensor_times = []
sensor_readings_pos = []
sensor_readings_vel = []

# Connect to cart and get user input on desired sample rate and display of actual sample rate
print('This program will Smart Cart position, velocity, and time in a 3-axis graph.')
cart_ID = input('Enter the ID of your Smart Cart: ')
print('Connecting...')
my_cart.connect_by_id(cart_ID)
print('Connected.')
period_s = 1/float(input('Enter the desired Smart Cart sample rate (Hz): '))    # convert provided sample rate in Hz to sample period in s
show_real_sample_rate = input('Would you like the actual sample rate displayed (y/n)? ').lower()

start_time = time.time()    # define the start time to later calculate elapsed experiment time
next_time = time.time() + period_s  # define the time for the first sample

while True:
    now = time.time()
    if now < next_time:     # do nothing if it's not yet time for a sample
        pass
    else:                   # take a sample if it's time or over time
        sensor_readings = my_cart.read_data_list(['Position', 'Velocity']) # read position and velocity from the cart
        sensor_times.append(now - (start_time + period_s))      # add elapsed experiment time to the end of the list
        sensor_readings_pos.append(sensor_readings['Position'])
        sensor_readings_vel.append(sensor_readings['Velocity'])
        next_time = now + period_s  # define the desired time for the next sample
        plot_graph(sensor_readings_pos, sensor_readings_vel, sensor_times) # send desired x, y, z lists to be graphed
        if show_real_sample_rate == 'y' and len(sensor_times) > 2:  # calculate and display approx actual sample rate if requested
            print(f'Actual sample rate (Hz): {round(1/(sensor_times[-1]-sensor_times[-2]))}')

