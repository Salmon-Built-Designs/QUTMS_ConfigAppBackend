import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import math
from main import log_idx

MAKE_GRAPHS = False

MAIN_DATA_FOLDER = "data_dump"
LOG_DATA_FOLDER = f"{MAIN_DATA_FOLDER}/{log_idx}"
RAW_DATA_FOLDER = f"{LOG_DATA_FOLDER}/raw"
GRAPH_FOLDER = f"{LOG_DATA_FOLDER}/graphs"

# https://stackoverflow.com/a/26026189
def find_nearest(array,value):
    idx = np.searchsorted(array, value, side="left")
    if idx > 0 and (idx == len(array) or math.fabs(value - array[idx-1]) < math.fabs(value - array[idx])):
        return idx
    else:
        return idx

# generate BMS data
BMS_COUNT = 12
TEMPERATURE_COUNT = 12
CELL_COUNT = 10

# cut off for bad temps when making graphs
INVALID_TEMP = 80

def save_bms_temps(bmsID, bms_data):
    f = open(f"{RAW_DATA_FOLDER}/bms_{bmsID}_temperatures.csv", 'w')
    times = np.array(bms_data[0]) / 1000

    header = 'time'
    for i in range(0, TEMPERATURE_COUNT):
        header = header + f', temp{i}'
    header = header + '\n'
    f.write(header)

    for i in range(0, len(times)):
        row = f'{times[i]}, '
        for j in range(0, TEMPERATURE_COUNT):
            if (bms_data[j+1][i]) != 0:
                row += f'{bms_data[j+1][i]}, '
            else:
                row += ","
        row += '\n'
        f.write(row)
    f.close()

def save_bms_voltages(bmsID, bms_data):
    f = open(f"{RAW_DATA_FOLDER}/bms_{bmsID}_voltages.csv", 'w')
    times = np.array(bms_data[0]) / 1000

    header = 'time'
    for i in range(0, CELL_COUNT):
        header = header + f', cell{i}'
    header = header + '\n'
    f.write(header)

    for i in range(0, len(times)):
        row = f'{times[i]}, '
        for j in range(0, CELL_COUNT):
            if (bms_data[j+1][i]) != 0:
                row += f'{bms_data[j+1][i]}, '
            else:
                row += ","
        row += '\n'
        f.write(row)
    f.close()

def plot_bms_temps(bmsID, bms_data):
    times = np.array(bms_data[0]) / 1000
    plt.figure()
    for i in range(0, TEMPERATURE_COUNT):
        temps = np.array(bms_data[i+1])
        valid_idx = (temps != 0) & (temps < INVALID_TEMP)
        plt.plot(times[valid_idx], temps[valid_idx])
    plt.title(f'bms {bmsID} temperatures')
    plt.xlabel("Time (s)")
    plt.ylabel("Celcius")

    plt.savefig(f'{GRAPH_FOLDER}/BMS_TEMPS_{bmsID}.png', format='png')
    plt.close()

def plot_bms_voltages(bmsID, bms_data):
    times = np.array(bms_data[0]) / 1000
    plt.figure()
    for i in range(0, CELL_COUNT):
        volts = np.array(bms_data[i+1])
        valid_idx = (volts != 0)
        plt.plot(times[valid_idx], volts[valid_idx])
    plt.title(f'bms {bmsID} voltages')
    plt.xlabel("Time (s)")
    plt.ylabel("mV")

    plt.savefig(f'{GRAPH_FOLDER}/BMS_VOLTAGES_{bmsID}.png', format='png')
    plt.close()

def extract_bms_temps(data):
    # setup initial arrays
    bms_temps = []
    for i in range(0, BMS_COUNT):
        blank_row = [[]]
        for j in range(0, TEMPERATURE_COUNT):
            blank_row.append([])
        bms_temps.append(blank_row)

    # shove data into raw python array
    for temp_pack in data:
        timestamp = temp_pack[0]
        bmsId = temp_pack[2]
        msgID = temp_pack[3]
        
        temperatures = temp_pack[4]
        bms_temps[bmsId][0].append(timestamp)
        temps = np.zeros(TEMPERATURE_COUNT)
        for i in range(0, len(temperatures)):
            temps[i + (int(TEMPERATURE_COUNT/2)*msgID)] = temperatures[i]

        for i in range(0, TEMPERATURE_COUNT):
            bms_temps[bmsId][i+1].append(temps[i])

    # save to file and plot
    for i in range(0, BMS_COUNT):
        bms_data = bms_temps[i]
        save_bms_temps(i, bms_data)
        if (MAKE_GRAPHS):
            plot_bms_temps(i, bms_data)

def extract_bms_volts(data):
    # setup initial arrays
    bms_volts = []
    for i in range(0, BMS_COUNT):
        blank_row = [[]]
        for j in range(0, CELL_COUNT):
            blank_row.append([])
        bms_volts.append(blank_row)

    # shove data into raw python array
    for volt_pack in data:
        timestamp = volt_pack[0]
        bmsId = volt_pack[2]
        msgID = volt_pack[3]        
        voltages = volt_pack[4]
        bms_volts[bmsId][0].append(timestamp)
        volts = np.zeros(CELL_COUNT)
        for i in range(0, len(voltages)):
            if ((i+msgID*4) < CELL_COUNT):
                volts[i + (msgID*4)] = voltages[i]

        for i in range(0, CELL_COUNT):
            bms_volts[bmsId][i+1].append(volts[i])

    # save to file and plot
    for i in range(0, BMS_COUNT):
        bms_data = bms_volts[i]
        save_bms_voltages(i, bms_data)
        if (MAKE_GRAPHS):
            plot_bms_voltages(i, bms_data)

# generate sendyne data
def extract_sendyne(data):
    # time, current
    current_data = [[], [], []]
    raw_coulomb_data = [[], [], []]

    for sendyne in data:
        timestamp = sendyne[0]
        id = sendyne[2]
        msg_request = int(sendyne[4],0)
        msg_type = sendyne[5]
        msg_data = sendyne[6]
        if (msg_type == 'Current'):
            current_row = [0,0,0]
            current_row[0] = timestamp
            current_row[id+1] = msg_data
            for i in range(0, len(current_row)):
                current_data[i].append(current_row[i])
        elif (msg_type.startswith('Coulomb Count')):
            # only first one should have coulomb
            if (id == 0):
                coulomb_row = [0,-1,-1]
                coulomb_row[0] = timestamp
                idx = (2,1)[msg_request == 0x40]
                coulomb_row[idx] = msg_data
                for i in range(0, len(coulomb_row)):
                    raw_coulomb_data[i].append(coulomb_row[i])

    # reformat coulomb data
    coulomb_data = calculate_coulomb_data(raw_coulomb_data)    

    # approximate current from coulomb count
    coulomb_current = extract_current_from_coulomb(coulomb_data)

    save_sendyne_current(current_data)
    save_sendyne_coulomb(coulomb_data, raw_coulomb_data)
    save_coulomb_current(coulomb_current)
    if (MAKE_GRAPHS):
        plot_sendyne_current(current_data)
        plot_sendyne_coulomb(coulomb_data)
        plot_coulomb_current(coulomb_current)

def calculate_coulomb_data(raw_coulomb_data):
    # yeet out high and low    
    coulomb_times = np.array(raw_coulomb_data[0])
    coulomb_low = np.array(raw_coulomb_data[1])
    coulomb_high = np.array(raw_coulomb_data[2])
    coulomb_low_idx = coulomb_low != -1
    coulomb_high_idx = coulomb_high != -1

    cc_low = [coulomb_times[coulomb_low_idx], coulomb_low[coulomb_low_idx]]
    cc_high = [coulomb_times[coulomb_high_idx], coulomb_high[coulomb_high_idx]]

    coulomb_data = [[],[]]
    for i in range(0, len(cc_low[0])):
        timestamp_l = cc_low[0][i]
        cc_l = cc_low[1][i]

        cc_h_idx = find_nearest(cc_high[0], timestamp_l)
        timestamp_h = cc_high[0][cc_h_idx]
        cc_h = cc_high[1][cc_h_idx]

        timestamp = (timestamp_l + timestamp_h) / 2
        cc = int(cc_h) | int(cc_l)

        coulomb_data[0].append(timestamp)
        coulomb_data[1].append(cc)

    # convert from micro coulombs to coulombs
    coulomb_data[1] = np.array(coulomb_data[1]) * 1e-6

    return coulomb_data

def extract_current_from_coulomb(coulomb_data):
    coulomb_current = [[],[]]
    times = np.array(coulomb_data[0])
    coulombs = np.array(coulomb_data[1])
    for i in range(0, len(coulomb_data[0])-1):
        timestep = times[i+1] - times[i]
        # set time for this approximation to be middle of two readings
        coulomb_current[0].append(times[i] + (timestep/2))

        current_approx = (coulombs[i+1] - coulombs[i])/timestep
        coulomb_current[1].append(current_approx)

    return coulomb_current

def save_coulomb_current(coulomb_current):
    f = open(f"{RAW_DATA_FOLDER}/sendyne_coulomb_current.csv", 'w')
    times = np.array(coulomb_current[0]) / 1000

    header = 'time, current\n'
    f.write(header)
    for i in range(0, len(times)):
        row = f'{times[i]}, {coulomb_current[1][i]}\n'
        f.write(row)
    f.close()

def save_sendyne_current(current_data):
    f = open(f"{RAW_DATA_FOLDER}/sendyne_current.csv", 'w')
    times = np.array(current_data[0]) / 1000

    header = 'time, current0, current1\n'
    f.write(header)

    for i in range(0, len(times)):
        row = f'{times[i]}'
        for j in range(1,3):
            if (current_data[j][i] != 0):
                row += f', {current_data[j][i]}'
            else:
                row += ","
        row += "\n"
        f.write(row)
    f.close() 

def save_sendyne_coulomb(coulomb_data, raw_coulomb_data):
    f = open(f"{RAW_DATA_FOLDER}/sendyne_coulomb.csv", 'w')
    times = np.array(coulomb_data[0]) / 1000

    header = 'time, coulomb_count\n'
    f.write(header)
    for i in range(0, len(times)):
        row = f'{times[i]}, {coulomb_data[1][i]}\n'
        f.write(row)
    f.close()

    f = open(f"{RAW_DATA_FOLDER}/sendyne_coulomb_RAW.csv", 'w')
    times = np.array(raw_coulomb_data[0]) / 1000

    header = 'time, coulomb_count_low, coulomb_count_high\n'
    f.write(header)

    for i in range(0, len(times)):
        row = f'{times[i]}'
        for j in range(1,3):
            if (raw_coulomb_data[j][i] != -1):
                row += f', {raw_coulomb_data[j][i]}'
            else:
                row += ","
        row += "\n"
        f.write(row)
    f.close() 

def plot_coulomb_current(coulomb_current):
    times = np.array(coulomb_current[0]) / 1000
    plt.figure()
    current = np.array(coulomb_current[1])
    plt.plot(times, current)
    plt.title(f'coulomb count current approximation')
    plt.xlabel("Time (s)")
    plt.ylabel("Current (A)")

    plt.savefig(f'{GRAPH_FOLDER}/SENDYNE_COULOMB_CURRENT.png', format='png')
    plt.close()

def plot_sendyne_coulomb(coulomb_data):
    times = np.array(coulomb_data[0]) / 1000
    plt.figure()
    coulombs = np.array(coulomb_data[1])
    plt.plot(times, coulombs)
    plt.title(f'sendyne coulomb count')
    plt.xlabel("Time (s)")
    plt.ylabel("Coulombs")

    plt.savefig(f'{GRAPH_FOLDER}/SENDYNE_COULOMB.png', format='png')
    plt.close()

def plot_sendyne_current(current_data):
    for cur in range(1,3):
        times = np.array(current_data[0]) / 1000
        plt.figure()
        currents = np.array(current_data[cur])
        valid_idx = (currents != 0)
        plt.plot(times[valid_idx], currents[valid_idx])
        plt.title(f'sendyne {cur-1} current')
        plt.xlabel("Time (s)")
        plt.ylabel("Current (A)")

        plt.savefig(f'{GRAPH_FOLDER}/SENDYNE_CURRENT_{cur-1}.png', format='png')
        plt.close()

# generate inverter data
def extract_inverters(inverter_data):
    throttle_cmds = [[],[]]
    brake_cmds = [[],[]]

    for msg in inverter_data:
        timestamp = msg[0]
        variable_number = msg[6]
        command = msg[7]
        index = int(msg[4],0)
        if (index == 0x2005):
            if (variable_number == 1):
                throttle_cmds[0].append(timestamp)
                throttle_cmds[1].append(command)
            elif (variable_number == 2):
                brake_cmds[0].append(timestamp)
                brake_cmds[1].append(command)

    #print(throttle_cmds)
    #print(brake_cmds)