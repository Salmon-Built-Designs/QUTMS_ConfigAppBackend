from flask import jsonify, json
import os
import uuid
import numpy as np
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from backend.can_ids import *
from backend import app, db, guard, models
from backend.models import Log

# Receive list of messages and split into packets
class log_container:
    def __init__(self, parsed_msgs):

        self.__id = self.__save_db()
        self.msgs = parsed_msgs
        
        self.bms_voltages = None
        self.bms_temps = None
        self.ams_volts = None
        self.ams_runtime = None
        self.sendyne_coulombs = None
        self.sendyne_current = None
    
    def request_msgs(self, req_type):
        requested_msgs = self.msgs

        if type == None:
            return requested_msgs
        else:
            # Filter to msg type
            requested_msgs = [ msg for msg in requested_msgs if (msg.msg_type in req_type)]
            return requested_msgs

    def save(self):
        #DUMP_FOLDER = 'export'
        DOCKER_VOLUME = "/var/lib/docker/volumes/qutms_configappbackend_log_storage/"

        if not os.path.exists(f'{DOCKER_VOLUME}/{str(self.id)}'):
            os.mkdir(f'{DOCKER_VOLUME}/{str(self.id)}')

        # Save msgs

        for i in range(len(self.bms_voltages)):
            file_path = fr'{DOCKER_VOLUME}/{self.__id}/BMSvoltages_{i}.csv'
            self.bms_voltages[i].to_csv(file_path, header=True)

    def __save_db(self):
        new_db_log = Log(driver='Lando', location='Brisbane', date_recorded=1234, description='driving around yeah')
        db.session.add(new_db_log)
        db.session.commit()

        return new_db_log.id

    @property
    def id(self):
        return self.__id
            