from smbus2 import SMBus
import time
import math

# I2C address of the device
MAGNETOMETER_ADDRESS = 0x1c  
# Define the register address where the LSB is stored
OUT_X_L = 0x28  # X LSB component of data
OUT_Y_L = 0X2a

# Register addresses
CTRL_REG1 = 0X20
CTRL_REG2 = 0X21
CTRL_REG3 = 0X22

# Register configurations
CONFIG_REG1 = 0X32
CONFIG_REG2 = 0X40
CONFIG_REG3 = 0X00

# Create an SMBus instance
bus = SMBus(1)  # 1 indicates /dev/i2c-1

def read_x_magnetometer():
    # Read 2 bytes of data from the magnetometer
    data_x = bus.read_i2c_block_data(MAGNETOMETER_ADDRESS, OUT_X_L, 2)
    # Combine the bytes assuming the LSB is at the lower address
    value = (data_x[1] << 8) | data_x[0]
    # Convert to signed value
    if value > 32767:
        value -= 65536
    return value
    
def read_y_magnetometer():
    # Read 2 bytes of data from the magnetometer
    data_y = bus.read_i2c_block_data(MAGNETOMETER_ADDRESS, OUT_Y_L, 2)
    # Combine the bytes assuming the LSB is at the lower address
    value = (data_y[1] << 8) | data_y[0]
    # Convert to signed value
    if value > 32767:
        value -= 65536
    return value
    
def configure_registers():
    # Write to the configuration register
    write_register(CTRL_REG1, CONFIG_REG1)
    # Read back from the data register
    data = read_register(CTRL_REG1)
    
    write_register(CTRL_REG2, CONFIG_REG2)
    data = read_register(CTRL_REG2)

    write_register(CTRL_REG3, CONFIG_REG3)
    data = read_register(CTRL_REG3)
    
def write_register(register, value):
    # Write an 8-bit value to the specified register
    bus.write_byte_data(MAGNETOMETER_ADDRESS, register, value)
    print(f'Wrote {value:#02x} to register {register:#02x}\n')

def read_register(register):
    # Read an 8-bit value from the specified register
    value = bus.read_byte_data(MAGNETOMETER_ADDRESS, register)
    print(f'Read {value:#02x} from register {register:#02x}\n')
    return value

def calculate_heading(x, y):
    # Calculate the angle in degrees
    angle = math.atan2(y, x) * (180 / math.pi)
    if angle < 0:
        angle += 360
    return angle

def display_compass(angle):
    directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW", "N"]
    index = round(angle / 45)
    return directions[index]

def compensate_hard_iron(x_raw, y_raw, x_max, x_min, y_max, y_min):
    x_offset = (x_max + x_min) / 2
    y_offset = (y_max + y_min) / 2
    
    x_corrected = x_raw - x_offset
    y_corrected = y_raw - y_offset
    
    return x_corrected, y_corrected

def auto_calibrate(duration=65):
    print("Starting auto-calibration. Please spin the device slowly in a circle.")
    
    start_time = time.time()
    x_min, x_max = float('inf'), float('-inf')
    y_min, y_max = float('inf'), float('-inf')
    
    while time.time() - start_time < duration:
        mag_x_data = read_x_magnetometer()
        mag_y_data = read_y_magnetometer()
        
        if mag_x_data < x_min:
            x_min = mag_x_data
        if mag_x_data > x_max:
            x_max = mag_x_data
        
        if mag_y_data < y_min:
            y_min = mag_y_data
        if mag_y_data > y_max:
            y_max = mag_y_data
        
        # Calculate remaining time and print countdown
        remaining_time = duration - (time.time() - start_time)
        print(f"Calibrating... {int(remaining_time)} seconds remaining", end='\r')
        
        time.sleep(0.1)
    
    print(f"\nCalibration complete.\nX_min: {x_min}, X_max: {x_max}\nY_min: {y_min}, Y_max: {y_max}")
    return x_min, x_max, y_min, y_max

try:
    # Configure the registers
    configure_registers()
    
    # Auto-calibrate the magnetometer
    x_min, x_max, y_min, y_max = auto_calibrate()
    
    while True:
        # Continuously read data from the magnetometer
        mag_x_data = read_x_magnetometer()
        mag_y_data = read_y_magnetometer()
        
        # Compensate for hard iron distortion
        mag_x_data, mag_y_data = compensate_hard_iron(mag_x_data, mag_y_data, x_max, x_min, y_max, y_min)
        
        # Calculate heading
        heading = calculate_heading(mag_x_data, mag_y_data)
        compass_direction = display_compass(heading)
        
        # Display data
        print(f"Raw X: {mag_x_data + ((x_max + x_min) / 2)}, Raw Y: {mag_y_data + ((y_max + y_min) / 2)}")
        print(f"Corrected X: {mag_x_data}, Corrected Y: {mag_y_data}")
        print(f"X_min: {x_min}, X_max: {x_max}")
        print(f"Y_min: {y_min}, Y_max: {y_max}")
        print(f"Heading: {heading:.2f} degrees, Direction: {compass_direction}\n")
        
        # Wait for a short period before reading again
        time.sleep(0.5)

except KeyboardInterrupt:
    # Clean up on interrupt (Ctrl+C)
    bus.close()
    print("\nProgram terminated.")
