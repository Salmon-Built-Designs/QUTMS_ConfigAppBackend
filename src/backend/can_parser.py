from flask import jsonify, json
import os
import uuid
import numpy as np
import pandas as pd
from backend.log_container import *
from backend.can_ids import *


# Object to contain all raw message information
class raw_can_msg:
    def __init__(
        self,
        timestamp: int,
        id: int,
        is_extended_id: bool,
        data_length: int,
        data: bytearray,
    ):
        self.timestamp = timestamp
        self.id = id
        self.is_extended_id = is_extended_id
        self.data_length = data_length
        self.data = data

    def __str__(self):
        return f"[{self.timestamp}]: [{hex(self.id)}, [{self.data}]]"


# Object to contain message relevant information read to be jsonified
# Message can be left blank if there is none
class split_can_msg:
    def __init__(
        self,
        timestamp,
        msg_type,
        message="",
    ):
        self.timestamp = timestamp
        self.msg_type = msg_type
        self.message = message

    # @property
    # def time(self):
    #     return self.timestamp

    def to_array(self):
        return np.array([self.timestamp, self.msg_type, self.message],dtype=object)

    def __str__(self):
        return f"[{self.timestamp}ms]:" + self.msg_type + " | " + str(self.message)

def process_file(path):
    if not os.path.exists(path):
        print("log file doesn't exist")
        return

    # Process the raw binary file into a list of objects
    raw_msgs = read_log_file(path)
    print(len(raw_msgs), "data entries found.")

    # Parse messages to create readable information
    # Create new log container with messages
    new_log = log_container(parse_can_msgs(raw_msgs))

    # Isolate voltages
    new_log.bms_voltages = compile_voltages(raw_msgs)

    # Isolate temperatures


    #Save
    new_log.save()

    print("All messages parsed")

    # Return list of message object ready to be turned into JSON
    return new_log
    


# Read binary file and add all messages to a list
def read_log_file(path):
    raw_msgs = []

    with open(path, "rb") as log_file:
        buffer = log_file.read(4)
        while buffer:
            buffer = list(buffer)
            # Concatanate bytes together
            timestamp = (
                (buffer[0]) | (buffer[1] << 8) | (
                    buffer[2] << 16) | (buffer[3] << 24)
            )

            # Read next byte for id type
            buffer = list(log_file.read(1))
            id_type = buffer[0] == 1

            # Read next 4 bytes for id
            buffer = list(log_file.read(4))
            id = (
                (buffer[0] << 0)
                | (buffer[1] << 8)
                | (buffer[2] << 16)
                | (buffer[3] << 24)
            )

            # Read next byte for data length
            buffer = list(log_file.read(1))
            dlc = buffer[0]

            # Read data based on data length
            buffer = list(log_file.read(dlc))
            data = buffer

            # Create object containing message data and add it to the raw messages list
            raw_msg = raw_can_msg(timestamp, id, id_type, dlc, data)
            raw_msgs.append(raw_msg)

            buffer = log_file.read(4)
    return raw_msgs


# PDM MESSAGES (Power Distribution Module)


def parse_pdm_startup(msg: raw_can_msg):
    # return (msg.timestamp, "PDM_InitiateStartup")
    return split_can_msg(msg.timestamp, "PDM_InitiateStartup")


def parse_pdm_startupok(msg: raw_can_msg):
    channels = (
        msg.data[0] | (msg.data[1] << 8) | (
            msg.data[2] << 16) | (msg.data[3] << 24)
    )
    return split_can_msg(msg.timestamp, "PDM_StartupOk", bin(channels))


def parse_pdm_setchannels(msg: raw_can_msg):
    channels = (
        msg.data[0] | (msg.data[1] << 8) | (
            msg.data[2] << 16) | (msg.data[3] << 24)
    )
    return split_can_msg(msg.timestamp, "PDM_SetChannels", bin(channels))


def parse_pdm_setdutycycle(msg: raw_can_msg):
    channel = msg.data[0] & 0xF
    duty_cycle = msg.data[1]
    return split_can_msg(msg.timestamp, "PDM_SetDutyCycle", ["CHANNEL: ", channel,"DUTY_CYCLE: ", duty_cycle])


def parse_pdm_heartbeat(msg: raw_can_msg):
    channels = (
        msg.data[0] | (msg.data[1] << 8) | (
            msg.data[2] << 16) | (msg.data[3] << 24)
    )
    return split_can_msg(msg.timestamp, "PDM_Heartbeat", bin(channels))


# AMS MESSAGES (Accumulator Management System)


def parse_ams_startup(msg: raw_can_msg):
    return split_can_msg(msg.timestamp, "AMS_Startup")


def parse_ams_heartbeat(msg: raw_can_msg):
    HVAn = (msg.data[0] & 0x1) > 0
    HVBn = (msg.data[0] & 0x2) > 0
    precharge = (msg.data[0] & 0x4) > 0
    HVAp = (msg.data[0] & 0x10) > 0
    HVBp = (msg.data[0] & 0x20) > 0
    initialised = (msg.data[0] & 0x80) > 0
    av_voltage = ((msg.data[1] & 0x3F) << 6) | msg.data[0]
    runtime = ((msg.data[3]) << 8) | msg.data[2]
    return split_can_msg(
        msg.timestamp,
        "AMS_Heartbeat",
        [
            f"runtime: {runtime} ",
            f"voltage: {av_voltage} ",
            f"HVAn: {HVAn}, HVAp: {HVAp}, HVBn: {HVBn}, HVABp: {HVBp}, precharge: {precharge}, init: {initialised}",
        ],
    )


def parse_ams_ready(msg: raw_can_msg):
    return split_can_msg(msg.timestamp, "AMS_Ready")


# CC MESSAGES (Chassis Controller)


def parse_cc_rtd(msg: raw_can_msg):
    return split_can_msg(msg.timestamp, "CC_RTD")


def parse_cc_fatal_shutdown(msg: raw_can_msg):
    return split_can_msg(msg.timestamp, "CC_FATAL_SHUTDOWN")


def parse_cc_soft_shutdown(msg: raw_can_msg):
    return split_can_msg(msg.timestamp, "CC_SOFT_SHUTDOWN")


# BMS MESSAGES (Battery Management System)

def parse_bms_transmit_voltage(msg: raw_can_msg):
    bmsID = msg.id & 0xF
    msgID = (msg.data[0] >> 6) & 0x3
    voltages = []
    for i in range(0, int(msg.data_length / 2)):
        v_h = (int(msg.data[2 * i + 1] & 0x3F)) << 6
        v_l = int(msg.data[2 * i]) & 0x3F
        voltage = v_h | v_l
        voltages.append(voltage)
    
    str_voltages = [str(int) for int in voltages]
    str_voltages = ", ".join(str_voltages)

    return split_can_msg(msg.timestamp, "BMS_TransmitVoltage", ["ID: ", bmsID, " ","MSG_ID: " , msgID, " VOLT: ", str_voltages])

def parse_bms_transmit_temperature(msg: raw_can_msg):
    bmsID = msg.id & 0xF
    msgID = msg.data[0] & 0x1
    temperatures = []
    for i in range(1, msg.data_length - 1):
        temperatures.append(msg.data[i])

    str_temps = [str(int) for int in temperatures]
    str_temps = ", ".join(str_temps)

    return split_can_msg(
        msg.timestamp, "BMS_TransmitTemperature", ["BMSID: ", bmsID," MSGID: ", msgID," TEMPS: ", str_temps]
    )


def parse_bms_bad_cell_temperature(msg: raw_can_msg):
    bmsID = msg.id & 0xF
    cell = (msg.data[0] >> 4) & 0xF
    msgID = msg.data[0] & 0xF
    temperature = msg.data[1]   

    return split_can_msg(
        msg.timestamp,
        "BMS_BadCellTemperature",
        ["BMSID: ", bmsID,"MSGID: ", msgID,"CELL: ", cell,"TEMP: ", temperature],
    )


# INVERTER MSGS

INVERTER_ID = 0x600
INVERTER_QUERY_MASK = 0x3FE00
INVERTER_NODE_MASK = 0x1FF


def parse_cc_inverter(msg: raw_can_msg):
    nodeId = msg.id & INVERTER_NODE_MASK
    variableNumber = msg.data[3]
    clientCMDSpecifier = msg.data[0]
    index = msg.data[1] | (msg.data[2] << 8)
    msgType = "Unspecified Inverter Message"
    command = (
        msg.data[4] | (msg.data[5] << 8) | (
            msg.data[6] << 16) | (msg.data[7] << 24)
    )

    if index == 0x2005:
        msgType = "SetVariable"
    elif index == 0x2015:
        msgType = "SetBool"
        command = bin(command)
    elif index == 0x200C:
        msgType = "ShutdownInverter"
    elif index == 0x2000:
        msgType = "MotorCommand"

    return split_can_msg(
        msg.timestamp,
        "CC_Inverter",
        [
            hex(nodeId),
            bin(clientCMDSpecifier),
            hex(index),
            msgType,
            variableNumber,
            command,
        ],
    )


# SHUTDOWN
def parse_shdn_triggered(msg: raw_can_msg):
    return split_can_msg(msg.timestamp, "SHDN_Triggered")


def parse_shdn_heartbeat(msg: raw_can_msg):
    shdn_id = (msg.id & CAN_MASK_EXTRA) >> 4
    segmentStates = msg.data[0]
    return split_can_msg(msg.timestamp, "SHDN_Heartbeat", [shdn_id, bin(segmentStates)])


# SENDYNE SENSOR (Current & Coulombs)
SENDYNE_ID = 0xA100200
SENDYNE_REG_V1 = 0x60
SENDYNE_REG_CC_LOW = 0x40
SENDYNE_REG_CC_HIGH = 0x41
SENDYNE_REG_CURRENT = 0x20


def parse_sendyne(msg: raw_can_msg):
    msg.id = (msg.id & 0xFFFFFFF) | ((msg.id & ~0xFFFFFFF) >> 27)
    id = (msg.id >> 1) & 0x1
    request = msg.id & 0x1
    register = msg.data[0]
    data = 0
    msg_type = "Sendyne Undefined"

    if register == SENDYNE_REG_V1:
        msg_type = "Voltage 1"
        if request == 0:
            voltage = (
                (msg.data[1] << 24)
                | (msg.data[2] << 16)
                | (msg.data[3] << 8)
                | (msg.data[4])
            )
            data = voltage / 10 ** 6
    elif register == SENDYNE_REG_CURRENT:
        msg_type = "Current"
        if request == 0:
            current = (
                (msg.data[1] << 24)
                | (msg.data[2] << 16)
                | (msg.data[3] << 8)
                | (msg.data[4])
            )
            data = current / 10 ** 6
    elif register == SENDYNE_REG_CC_LOW:
        msg_type = "Coulomb Count (Low)"
        if request == 0:
            cc = (
                (msg.data[1] << 24)
                | (msg.data[2] << 16)
                | (msg.data[3] << 8)
                | (msg.data[4])
            )
            data = cc
    elif register == SENDYNE_REG_CC_HIGH:
        msg_type = "Coulomb Count (High)"
        if request == 0:
            cc = (
                (msg.data[1] << 56)
                | (msg.data[2] << 48)
                | (msg.data[3] << 40)
                | (msg.data[4] << 32)
            )
            data = cc

    return split_can_msg(
        msg.timestamp,
        "Sendyne",
        [id, hex(request), hex(register)," ", msg_type, " ", data, " ", msg.data],
    )


# Takes the raw messages and parses them according to their ID and
# returns a list of parsed messages in time order
def parse_can_msgs(msgs):
    bms_temps = []
    bms_voltages = []
    inverter_cmds = []
    sendyne_readings = []

    parsed_msgs = []
    # split_msgs = []

    print("Parsing CAN messages..")

    for msg in msgs:
        parsed = None
        id_no_bmsid = msg.id & (~0b1111)  # Ignore last 4 bits
        if id_no_bmsid == PDM_InitiateStartup_ID:
            parsed = parse_pdm_startup(msg)

        elif id_no_bmsid == PDM_StartupOk_ID:
            parsed = parse_pdm_startupok(msg)

        elif id_no_bmsid == PDM_SetChannelStates_ID:
            parsed = parse_pdm_setchannels(msg)

        elif id_no_bmsid == PDM_SetDutyCycle_ID:
            parsed = parse_pdm_setdutycycle(msg)

        elif id_no_bmsid == PDM_Heartbeat_ID:
            parsed = parse_pdm_heartbeat(msg)

        elif id_no_bmsid == AMS_StartUp_ID:
            parsed = parse_ams_startup(msg)

        elif id_no_bmsid == AMS_HeartbeatResponse_ID:
            parsed = parse_ams_heartbeat(msg)

        elif id_no_bmsid == AMS_Ready_ID:
            parsed = parse_ams_ready(msg)

        elif id_no_bmsid == BMS_TransmitVoltage_ID:
            parsed = parse_bms_transmit_voltage(msg)
            bms_voltages.append(parsed)

        elif id_no_bmsid == BMS_TransmitTemperature_ID:
            parsed = parse_bms_transmit_temperature(msg)
            bms_temps.append(parsed)

        elif id_no_bmsid == BMS_BadCellTemperature_ID:
            parsed = parse_bms_bad_cell_temperature(msg)

        elif (msg.is_extended_id == False) and (
            (msg.id & INVERTER_QUERY_MASK) == INVERTER_ID
        ):
            # inverter msgs
            parsed = parse_cc_inverter(msg)
            inverter_cmds.append(parsed)

        elif ((msg.id & ~0xFF) & 0xFFFFFFF) == SENDYNE_ID:
            parsed = parse_sendyne(msg)
            sendyne_readings.append(parsed)

        elif (msg.id & ~CAN_MASK_EXTRA) == SHDN_Heartbeat_ID:
            parsed = parse_shdn_heartbeat(msg)

        elif id_no_bmsid == SHDN_Triggered_ID:
            parsed = parse_shdn_triggered(msg)

        elif id_no_bmsid == CC_ReadyToDrive_ID:
            parsed = parse_cc_rtd(msg)

        elif id_no_bmsid == CC_SoftShutdown_ID:
            parsed = parse_cc_soft_shutdown(msg)

        elif id_no_bmsid == CC_FatalShutdown_ID:
            parsed = parse_cc_fatal_shutdown(msg)

        else:
            parsed = str(msg)
            print("Unknown entry found: " + parsed)
            print("Message was not added to the list")
            parsed = None

        parsed_array = parsed.to_array()
        parsed_msgs.append(parsed_array)
        

    msgs_array = np.stack(parsed_msgs,axis=0)

    msg_dataframe = pd.DataFrame(data=msgs_array, columns=['timestamp', 'message type', 'message'])
    msg_dataframe.set_index("timestamp", inplace=True)

    return msg_dataframe

def compile_voltages(msgs):

    empty_cells = np.empty((4,11))
    empty_cells[:] = np.nan
    voltage_cache = np.copy(empty_cells)

    #voltage_data = [[], [], [], []]
    voltage_data = []

    for msg in msgs:
        id_no_bmsid = msg.id & (~0b1111)  # Ignore last 4 bits
        if id_no_bmsid == BMS_TransmitVoltage_ID:
                bmsID = msg.id & 0xF
                msgID = (msg.data[0] >> 6) & 0x3
                voltages = []
                for i in range(0, int(msg.data_length / 2)):
                    v_h = (int(msg.data[2 * i + 1] & 0x3F)) << 6
                    v_l = int(msg.data[2 * i]) & 0x3F
                    voltage = v_h | v_l
                    voltages.append(voltage)
                
                # Start of a new voltage reading, record timestamp
                if msgID == 0:
                    voltage_cache[bmsID][0] = msg.timestamp

                # Remove last 2 excess zeros from the voltage readout
                if msgID == 2:
                    voltages = voltages[:len(voltages)-2]

                # add voltages to cache. start one over to leave room for timestamp, shift over depending on msgID
                for i in range(len(voltages)):
                    voltage_cache[bmsID][1+(msgID*4 + i)] = voltages[i]

                # Voltage data overflow at msgID, store full readout and clear cache
                if msgID == 2:
                    while (len(voltage_data) - 1 < bmsID):
                        voltage_data.append([])
                    #if (len(voltage_data) - 1 < bmsID): 
                        #voltage_data.append([])

                    voltage_data[bmsID].append(np.copy(voltage_cache[bmsID,:]))
                    voltage_cache[bmsID,:] = np.nan

                
    volt_dataframes = []
    cols = ["timestamp"] + list(range(1,11))

    # Create panda dataframes for each voltage data set
    for i in range(len(voltage_data)):
        if len(voltage_data[i]) > 1:
            volt_array = np.stack(voltage_data[i],axis=0)
        else:
            volt_array = np.array(voltage_data[i])

        volt_dataframe = pd.DataFrame(data=volt_array, columns=cols)
        volt_dataframe.set_index("timestamp", inplace=True)

        volt_dataframes.append(volt_dataframe)

    return volt_dataframes



                

                
                
