import pyvisa
import time
import numpy as np
# path to folder to save text file measurement data
path_to_folder = 'd:/Python/Ametek_DSP_7270_signal_recovery/single_channel_A_volatge_monitoring/text_file/'
# path to text file to save data
path_to_file = path_to_folder + 'ametek_dsp_7270_volatge_meas.txt'
# start pyVISA Resource manager
rm = pyvisa.ResourceManager()
print(rm)
# acquire and print possible connections
rm.list_resources()
print(rm.list_resources())
# open TCPIP SOCKET connection to the Ametek DSP 7270 Signal Recovery lock-in
ametek_inst = rm.open_resource('TCPIP0::147.213.112.60::50000::SOCKET')
# termination characters for reading and writing
ametek_inst.read_termination = '\r\n'
ametek_inst.write_termination = '\r\n'
# set reference input
# set reference to internal input = 0
# set reference to external rear panel input = 1
# set reference to external front panel input = 2
ametek_inst.write('IE 2')
time.sleep(1)
# select current / voltage mode input selector
# current mode off, voltage mode input enabled
ametek_inst.write('IMODE 0')
time.sleep(1)
# full scale sensitivity control
ametek_inst.write('SEN 11')
time.sleep(1)
# set voltage input configuration
# channel A = 1
ametek_inst.write('VMODE 1')
time.sleep(1)
### set AC gain control to automatic mode = 1
##ametek_inst.write('AUTOMATIC 1')
# set AC gain control to manual mode = 0
ametek_inst.write('AUTOMATIC 0')
time.sleep(1)
# set AC gain to 0 dB
ametek_inst.write('ACGAIN 0')
time.sleep(1)
# input connector shield float / ground control
# equal to 0 (ground)
# equal to 1 (conncted to ground via 1 kOhm resistor)
ametek_inst.write('FLOAT 0')
time.sleep(1)
# turn off line frequency rejection filter
ametek_inst.write('LF 0 0')
time.sleep(1)
# set time constant to 10 seconds
ametek_inst.write('TC 18')
time.sleep(1)
# set auto phase (auto quadrature null)
# the instrument adjust the refernec phase to maximize X and minimize Y
ametek_inst.write('AQN')
time.sleep(1)
# create buffer to store measurement data as numpy array
buffer = np.array([], dtype=float)
# create buffer for actual measurement
single_meas = np.zeros([1,6], dtype=float)
# wait time between voltage measurememts in seconds
wait_time = 1.0
# create counter to count measurement
counter = 1
# wait additional time for settting lock-in parameters
time.sleep(5)
# main loop
while True:
    # reads Magnitude value in Volts
    ametek_inst.write('MAG.')
    data_mag = ametek_inst.read_raw()
    #print(data_mag)
    #print(list(data_mag))
    data_mag_len=len(data_mag)
    for index_0 in range(data_mag_len):
        if (data_mag[index_0] == 0):
            last_zero=index_0
            #print(last_zero)
    data_mag_seleced_bytes=data_mag[(last_zero+1):(data_mag_len-1)]
    try:
        mag_value=float(data_mag_seleced_bytes.decode('utf-8'))
    except:
        mag_value=9.99999999999E+06
    #print(mag_value)
    #time.sleep(wait_time/5)
    time.sleep(0.01)
    # reads Phase value in degrees
    ametek_inst.write('PHA.')
    data_pha = ametek_inst.read_raw()
    #print(data_pha)
    #print(list(data_pha))
    data_pha_len=len(data_pha)
    for index_0 in range(data_pha_len):
        if (data_pha[index_0] == 0):
            last_zero=index_0
            #print(last_zero)
    data_pha_seleced_bytes=data_pha[(last_zero+1):(data_pha_len-1)]
    try:
        pha_value=float(data_pha_seleced_bytes.decode('utf-8'))
    except:
        pha_value=9.99999999999E+06
    #print(pha_value)
    #time.sleep(wait_time/5)
    time.sleep(0.01)
    # reads X value in Volts
    ametek_inst.write('X.')
    data_x = ametek_inst.read_raw()
    #print(data_x)
    #print(list(data_x))
    data_x_len=len(data_x)
    for index_0 in range(data_x_len):
        if (data_x[index_0] == 0):
            last_zero=index_0
            #print(last_zero)
    data_x_seleced_bytes=data_x[(last_zero+1):(data_x_len-1)]
    try:
        x_value=float(data_x_seleced_bytes.decode('utf-8'))
    except:
        x_value=9.99999999999E+06
    #print(x_value)
    #time.sleep(wait_time/5)
    time.sleep(0.01)
    # reads Y value in Volts
    ametek_inst.write('Y.')
    data_y = ametek_inst.read_raw()
    #print(data_y)
    #print(list(data_y))
    data_y_len=len(data_y)
    for index_0 in range(data_y_len):
        if (data_y[index_0] == 0):
            last_zero=index_0
            #print(last_zero)
    data_y_seleced_bytes=data_y[(last_zero+1):(data_y_len-1)]
    try:
        y_value=float(data_y_seleced_bytes.decode('utf-8'))
    except:
        y_value=9.99999999999E+06
    #print(y_value)
    #time.sleep(wait_time/5)
    time.sleep(0.01)
    # reads Frequency value in Volts
    ametek_inst.write('FRQ.')
    data_frq = ametek_inst.read_raw()
    #print(data_frq)
    #print(list(data_frq))
    data_frq_len=len(data_frq)
    for index_0 in range(data_frq_len):
        if (data_frq[index_0] == 0):
            last_zero=index_0
            #print(last_zero)
    data_frq_seleced_bytes=data_frq[(last_zero+1):(data_frq_len-1)]
    try:
        frq_value=float(data_frq_seleced_bytes.decode('utf-8'))
    except:
        frq_value=9.99999999999E+06
    frq_value=float(data_frq_seleced_bytes.decode('utf-8'))
    #print(frq_value)
    #time.sleep(wait_time/5)
    time.sleep(0.01)
    # insert measured values to the single measuremnet buffer
    single_meas[0][0] = float(float(counter)*wait_time)
    single_meas[0][1] = float(mag_value)
    single_meas[0][2] = float(pha_value)
    single_meas[0][3] = float(x_value)
    single_meas[0][4] = float(y_value)
    single_meas[0][5] = float(frq_value)
    # print measured data
    print(single_meas)
    # append single measurement data to buffer
    buffer = np.append(buffer, single_meas)
    #print(buffer)
    # increase counter
    counter += 1
    # size of buffer numpy array
    buffer_size = np.size(buffer)
    # print buffer size
    #print(buffer_size)
    no_rows =  int(buffer_size/6)
    # reshape buffer numpy array
    buffer_reshaped = np.reshape(buffer, (no_rows, 6))
    # save reshaped buffer numpy array
    np.savetxt(path_to_file, buffer_reshaped, delimiter='\t')
    # wait aditional time after fast reading of data
    time.sleep(wait_time-5*0.01)


