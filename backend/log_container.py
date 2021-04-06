import os
import numpy as np
import pandas as pd
from .can_ids import *
import pickle

# Receive list of messages and split into packets
class log_container:
    def __init__(self, parsed_msgs, metadata):
        self.__id = metadata[0]
        self.metadata = metadata
        self.msgs = parsed_msgs
        self.msgs_dataframe = self.__to_dataframe(self.msgs)
        
        self.bms_voltages = None
        self.bms_temps = None
        self.ams_volts = None
        self.ams_runtime = None
        self.sendyne_coulombs = None
        self.sendyne_current = None
    
    def request_msgs(self, req_type):
        requested_msgs = self.msgs

        if req_type == None:
            return requested_msgs
        else:
            # Filter to msg type
            requested_msgs = [ msg for msg in requested_msgs if (msg.msg_type in req_type)]
            return requested_msgs

    def request_data(self, req_type, id):
        if req_type == "BMS_TransmitVoltage":
            return self.bms_voltages[id].to_json(orient="records")

    def save(self):
        SAVE_VOLUME = "storage"
        
        file_path = fr'{SAVE_VOLUME}'
        log_path = fr'{SAVE_VOLUME}/{self.__id}/'

        if not os.path.exists(file_path):
            os.mkdir(file_path)

        if not os.path.exists(log_path):
            os.mkdir(log_path)

        # Save msgs
        self.msgs_dataframe.to_csv(log_path + fr'rawMsgs.csv', header=True)

        # Save voltages
        for i in range(len(self.bms_voltages)): 
            self.bms_voltages[i].to_csv(log_path + fr'BMSvoltages_{i}.csv', header=True, index=False)

        # Save metadata
        # with open(log_path + 'metadata.json', 'w') as output:
        #     output.write(self.metadata)

        # Save object as pickle
        with open(log_path + 'log_dump.pkl', 'wb') as output:  # Overwrites any existing file.
            pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)

    def __to_dataframe(self, msgs_list):
        msg_arrays = []

        for msg in msgs_list:
            msg_array = msg.to_array()
            msg_arrays.append(msg_array)

        msgs_stack = np.stack(msg_arrays,axis=0)

        msg_dataframe = pd.DataFrame(data=msgs_stack, columns=['timestamp', 'message type', 'message'])
        #msg_dataframe.set_index("timestamp", inplace=True)

        return msg_dataframe

    @property
    def id(self):
        return self.__id
            