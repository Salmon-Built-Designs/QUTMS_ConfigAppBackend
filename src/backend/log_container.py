from flask import jsonify, json
import os
import uuid
import numpy as np
import pandas as pd
from backend.can_ids import *

# Receive list of messages and split into packets
class log_container:
    def __init__(self, parsed_msgs):
        new_id = uuid.uuid1()
        self.__id = new_id.int
        self.msgs = parsed_msgs
        
        self.bms_voltages = None
        self.bms_temps = None
        self.ams_volts = None
        self.ams_runtime = None
        self.sendyne_coulombs = None
        self.sendyne_current = None
    
    def request_msgs(self, req_type):
        # Filter to time range
        #requested_msgs = [ msg for msg in self.msgs if (msg.timestamp >= start_time and  msg.timestamp <= end_time)]

        if type == None:
            return requested_msgs
        else:
            # Filter to msg type
            requested_msgs = [ msg for msg in requested_msgs if (msg.msg_type in req_type)]
            return requested_msgs

    def save(self):
        DUMP_FOLDER = 'export'

        if not os.path.exists(DUMP_FOLDER):
            os.mkdir(DUMP_FOLDER)

        if not os.path.exists(f'{DUMP_FOLDER}/{str(self.id)}'):
            os.mkdir(f'{DUMP_FOLDER}/{str(self.id)}')

        for i in range(len(self.bms_voltages)):
            file_path = fr'{DUMP_FOLDER}/{self.__id}/BMSvoltages_{i}.csv'
            self.bms_voltages[i].to_csv(file_path, header=True)

    @property
    def id(self):
        return self.__id
            