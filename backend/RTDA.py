import socket
from can_parser import *
from can_ids import *

# Setup TCP Connection for CAN1
TCP_IP = '192.168.0.7'
TCP_PORT_CAN1 = 20001
TCP_PORT_CAN2 = 20005 # Double check this
BUFFER_SIZE = 4096
ID_TYPE = 1

while True:
	# Connect to the TCP server
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((TCP_IP, TCP_PORT_CAN1))

	# Recieve any data that is available for us
	data = s.recv(BUFFER_SIZE)
	s.close()

	# Parse the data and unwrap key from metadata
	raw_msgs = []
	ethernetPacketInformation = data[0]
	dataLength = (ethernetPacketInformation & 0xF)
	# CAN ID
	canId = (data[1] << 24 | data[2] << 16 | data[3] << 8 | data[4] << 0)
	parsedData = data[5:dataLength+5]

	# Drop the messages into an array and parse them
	raw_msgs.append(raw_can_msg(0, canId, ID_TYPE, dataLength, parsedData))
	result = parse_can_msgs(raw_msgs, False)

	# Log
	print(result)