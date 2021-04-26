import socket
from .can_parser import *
from .can_ids import *
from .log_container import *
import logging

# Setup TCP Connection for CAN1
TCP_IP = '192.168.0.7'
TCP_PORT_CAN1 = 20001
TCP_PORT_CAN2 = 20005 # Double check this
BUFFER_SIZE = 4096
ID_TYPE = 1

def livetelemetry(metadata):
	logger = logging.getLogger('websockets')
	logger.setLevel(logging.INFO)
	logger.addHandler(logging.StreamHandler())

	# Connect to the TCP server
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((TCP_IP, TCP_PORT_CAN1))
	
	s.sendall(b'\x84\x10\x50\x80\x02\x01\x02\x04\x08\x00\x00\x00\x00')
	#s.sendall(b'\x84\x00\x00\x06\x78\x12\x34\x56\x78\x00\x00\x00\x00')
	# Receive any data that is available for us
	data = s.recv(BUFFER_SIZE)
	s.close()
	# Parse the data and unwrap key from metadata
	raw_msgs = []
	ethernetPacketInformation = data[0]
	dataLength = (ethernetPacketInformation & 0xF)
	# CAN ID
	canId = (data[1] << 24 | data[2] << 16 | data[3] << 8 | data[4] << 0)
	parsedData = data[5:dataLength+5]
	metadata = ['e007dff49c494105a9bdbd4852b25ef2', 'some description', 'some date', 'some driver', 'some location']
	# Drop the messages into an array and parse them
	raw_msgs.append(raw_can_msg(0, canId, ID_TYPE, dataLength, parsedData))

	result = log_container(parse_can_msgs(raw_msgs, False), metadata)

	result.save()

	return result

	# ['e007dff49c494105a9bdbd4852b25ef2', 'some description', 'some date', 'some driver', 'some location']