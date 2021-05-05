import numpy as np
import pandas as pd

BMS_COUNT = 12
TEMP_COUNT = 14
VOLT_COUNT = 10

current_bms_temp_data = np.zeros((BMS_COUNT, TEMP_COUNT))
current_bms_volt_data = np.zeros((BMS_COUNT, VOLT_COUNT))

bms_temp_data = []

def setup_storage():
    for i in range(BMS_COUNT):
        df = pd.DataFrame(columns = ["Time", "T0", "T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8", "T9", "T10", "T11", "T12", "T13", "T14"])
        bms_temp_data.append(df)

def add_bms_temp(timestamp, bms_id, msg_id, data):
    offset = msg_id * 6
    if msg_id < 2:
        current_bms_temp_data[bms_id, offset:offset+6] = np.array(data)
    elif msg_id == 2:
        print(current_bms_temp_data[bms_id, offset:TEMP_COUNT-1])
        current_bms_temp_data[bms_id, offset:TEMP_COUNT] = np.array(data)

        new_row = np.reshape(current_bms_temp_data[bms_id, :], (1,TEMP_COUNT))
        print(new_row)

        idx = len(bms_temp_data[bms_id][0])
        print(idx)
        print(bms_temp_data[bms_id][0])

        bms_temp_data[bms_id][0] = np.append(bms_temp_data[bms_id][0], timestamp, axis=1)
        bms_temp_data[bms_id][1] = np.append(bms_temp_data[bms_id][1], current_bms_temp_data[bms_id,:], axis=1)


    else:
        print(f"bad msg_id lmao {msg_id}")
       