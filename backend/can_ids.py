# Helper function to compose the CAN ID by concatenating
def Compose_CANId(priority, sourceId, autonomous, type, extra, BMSId):
    return ((priority & 0x3) << 27) | ((sourceId & 0x1FF) << 18) | ((autonomous & 0x1) << 17) | ((type & 0x7) << 14) | ((extra & 0x3FF) << 4) | (BMSId & 0xF)

# Define CAN numbers
CAN_PRIORITY_ERROR = 0x0
CAN_PRIORITY_HEARTBEAT = 0x1
CAN_PRIORITY_NORMAL = 0x2
CAN_PRIORITY_DEBUG = 0x3

CAN_SRC_ID_SHDN = 0x06
CAN_SRC_ID_AMS = 0x10
CAN_SRC_ID_BMS = 0x12
CAN_SRC_ID_PDM = 0x14
CAN_SRC_ID_CC = 0x16

CAN_TYPE_ERROR = 0x0
CAN_TYPE_HEARTBEAT = 0x1
CAN_TYPE_RECEIVE = 0x2
CAN_TYPE_TRANSMIT = 0x3
CAN_TYPE_STREAM = 0x7

CAN_MASK_EXTRA = (0x3FF << 4)

DRIVER = 0x00
DRIVERLESS = 0x01


# Create IDs
AMS_CellVoltageShutdown_ID 		= Compose_CANId(CAN_PRIORITY_ERROR, CAN_SRC_ID_AMS, DRIVER, 0x0, 0x0, 0x0)
AMS_CellTemperatureShutdown_ID 	= Compose_CANId(CAN_PRIORITY_ERROR, CAN_SRC_ID_AMS, DRIVER, 0x0, 0x1, 0x0)
AMS_MissingBMS_ID 				= Compose_CANId(CAN_PRIORITY_ERROR, CAN_SRC_ID_AMS, DRIVER, 0x0, 0x2, 0x0)
AMS_HeartbeatRequest_ID 		= Compose_CANId(CAN_PRIORITY_ERROR, CAN_SRC_ID_AMS, DRIVER, 0x1, 0x0, 0x0)
AMS_HeartbeatResponse_ID 		= Compose_CANId(CAN_PRIORITY_HEARTBEAT, CAN_SRC_ID_AMS, DRIVER, 0x1, 0x01, 0x0)
AMS_StartUp_ID					= Compose_CANId(CAN_PRIORITY_ERROR, CAN_SRC_ID_AMS, DRIVER, 0x2, 0x0, 0x0)
AMS_ResetTractive_ID			= Compose_CANId(CAN_PRIORITY_ERROR, CAN_SRC_ID_AMS, DRIVER, 0x2, 0x1, 0x0)
AMS_Shutdown_ID 				= Compose_CANId(CAN_PRIORITY_ERROR, CAN_SRC_ID_AMS, DRIVER, 0x2, 0x2, 0x0)
AMS_RequestTemperature_ID 		= Compose_CANId(CAN_PRIORITY_ERROR, CAN_SRC_ID_AMS, DRIVER, 0x2, 0x3, 0x0)
AMS_TransmitTemperature_ID		= Compose_CANId(CAN_PRIORITY_ERROR, CAN_SRC_ID_AMS, DRIVER, 0x3, 0x3, 0x0)
AMS_RequestChargeState_ID 		= Compose_CANId(CAN_PRIORITY_ERROR, CAN_SRC_ID_AMS, DRIVER, 0x2, 0x4, 0x0)
AMS_TransmitChargeState_ID 		= Compose_CANId(CAN_PRIORITY_ERROR, CAN_SRC_ID_AMS, DRIVER, 0x3, 0x4, 0x0)
AMS_Ready_ID					= Compose_CANId(CAN_PRIORITY_ERROR, CAN_SRC_ID_AMS, DRIVER, 0x3, 0x0, 0x0)

BMS_BadCellVoltage_ID 			= Compose_CANId(CAN_PRIORITY_ERROR, CAN_SRC_ID_BMS, DRIVER, CAN_TYPE_ERROR, 0x00, 0x00)
BMS_BadCellTemperature_ID		= Compose_CANId(CAN_PRIORITY_ERROR, CAN_SRC_ID_BMS, DRIVER, CAN_TYPE_ERROR, 0x01, 0x00)
BMS_TransmitVoltage_ID			= Compose_CANId(CAN_PRIORITY_NORMAL, CAN_SRC_ID_BMS, DRIVER, CAN_TYPE_TRANSMIT, 0x02, 0x00)
BMS_TransmitTemperature_ID 		= Compose_CANId(CAN_PRIORITY_NORMAL, CAN_SRC_ID_BMS, DRIVER, CAN_TYPE_TRANSMIT, 0x03, 0x00)
BMS_ChargeEnabled_ID			= Compose_CANId(CAN_PRIORITY_NORMAL, CAN_SRC_ID_BMS, DRIVER, CAN_TYPE_RECEIVE, 0x00, 0x00)
BMS_TransmitBalancing_ID		= Compose_CANId(CAN_PRIORITY_NORMAL, CAN_SRC_ID_BMS, DRIVER, CAN_TYPE_TRANSMIT, 0x04, 0x00)

CC_ReadyToDrive_ID 				= Compose_CANId(CAN_PRIORITY_NORMAL, CAN_SRC_ID_CC, DRIVER, 0x0, 0x0, 0x0)
CC_FatalShutdown_ID 			= Compose_CANId(CAN_PRIORITY_NORMAL, CAN_SRC_ID_CC, DRIVER, 0x0, 0x1, 0x0)
CC_SoftShutdown_ID				= Compose_CANId(CAN_PRIORITY_NORMAL, CAN_SRC_ID_CC, DRIVER, 0x0, 0x1, 0x1)

PDM_InitiateStartup_ID			= Compose_CANId(CAN_PRIORITY_NORMAL, CAN_SRC_ID_PDM, DRIVER, CAN_TYPE_RECEIVE, 0x00, 0x0)
PDM_StartupOk_ID 				= Compose_CANId(CAN_PRIORITY_NORMAL, CAN_SRC_ID_PDM, DRIVER, CAN_TYPE_TRANSMIT, 0x00, 0x0)
PDM_SelectStartup_ID			= Compose_CANId(CAN_PRIORITY_NORMAL, CAN_SRC_ID_PDM, DRIVER, CAN_TYPE_TRANSMIT, 0x01, 0x0)
PDM_SetChannelStates_ID 		= Compose_CANId(CAN_PRIORITY_NORMAL, CAN_SRC_ID_PDM, DRIVER, CAN_TYPE_RECEIVE, 0x02, 0x0)
PDM_Heartbeat_ID				= Compose_CANId(CAN_PRIORITY_HEARTBEAT, CAN_SRC_ID_PDM, DRIVER, CAN_TYPE_HEARTBEAT, 0x0, 0x0)
PDM_RequestDutyCycle_ID			= Compose_CANId(CAN_PRIORITY_NORMAL, CAN_SRC_ID_PDM, DRIVER, CAN_TYPE_RECEIVE, 0x3, 0x0)
PDM_SetDutyCycle_ID 			= Compose_CANId(CAN_PRIORITY_NORMAL, CAN_SRC_ID_PDM, DRIVER, CAN_TYPE_RECEIVE, 0x4, 0x0)
PDM_TransmitDutyCycle_ID		= Compose_CANId(CAN_PRIORITY_NORMAL, CAN_SRC_ID_PDM, DRIVER, CAN_TYPE_TRANSMIT, 0x4, 0x0)

SHDN_Triggered_ID               = Compose_CANId(CAN_PRIORITY_ERROR, CAN_SRC_ID_SHDN, DRIVER, CAN_TYPE_ERROR, 0x00, 0x00)
SHDN_Heartbeat_ID               = Compose_CANId(CAN_PRIORITY_HEARTBEAT, CAN_SRC_ID_SHDN, DRIVER, CAN_TYPE_HEARTBEAT, 0x00, 0x00)

id_list = [
    "AMS_CellVoltageShutdown",
    "AMS_CellTemperatureShutdown",
    "AMS_MissingBMS",
    "AMS_HeartbeatRequest",
    "AMS_HeartbeatResponse",
    "AMS_StartUp",
    "AMS_ResetTractive",
    "AMS_Shutdown",
    "AMS_RequestTemperature",
    "AMS_TransmitTemperature",
    "AMS_RequestChargeState" ,
    "AMS_TransmitChargeState" ,
    "AMS_Ready" ,
    "BMS_BadCellVoltage" ,
    "BMS_BadCellTemperature" ,
    "BMS_TransmitVoltage" ,
    "BMS_TransmitTemperature" ,
    "BMS_ChargeEnabled" ,
    "CC_ReadyToDrive" ,
    "CC_FatalShutdown" ,
    "CC_SoftShutdown" ,
    "PDM_InitiateStartup" ,
    "PDM_StartupOk" ,
    "PDM_SelectStartup" ,
    "PDM_SetChannelStates" ,
    "PDM_Heartbeat" ,
    "PDM_RequestDutyCycle" ,
    "PDM_SetDutyCycle" ,
    "PDM_TransmitDutyCycle" ,
    "SHDN_Triggered" ,
    "SHDN_Heartbeat" 
]