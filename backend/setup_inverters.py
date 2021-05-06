import math
import socket
import time
def setup_tpdo():

    # print(f"idx: {idx} tpdo: {tpdo_num}")
    # object_type = 0b10000000 | (tpdo_num << 8)
    # ethernet = 0b11001000

    # id = object_type + node_id
    # id_bytes = id.to_bytes(4, byteorder="little")

    tpdo_num = 1

    transmit = []

    header = [0xC8, 0x01,0x60,0x00,0x00]
    data = [0x40, 0x05, 0x21, 0x01, 0x0A, 0x00, 0x00, 0x00]

    transmit.extend(header)
    transmit.extend(data)

    # header = [0xC8, 0xE4,0x01,0x00,0x00]

    # # destroy TPDO
    # data = [0x23, 0x00, 0x18, 0x01, 0x81, 0x01, 0x00, 0xC0]

    # transmit.extend(header)
    # transmit.extend(data)

    # # destroy disable TPDO
    # data = [0x23, 0x00, 0x1A, 0x00, 0x00, 0x00, 0x00, 0x00]

    # transmit.extend(header)
    # transmit.extend(data)

    # # BC 0x2105

    # # ch 1
    # data = [0x23, 0x00, 0x1A, 0x01, 0x20, 0x01, 0x05, 0x21]

    # transmit.extend(header)
    # transmit.extend(data)

    # # ch 2
    # data = [0x23, 0x00, 0x1A, 0x02, 0x20, 0x02, 0x05, 0x21]

    # transmit.extend(header)
    # transmit.extend(data)

    # # set number of entires
    # data = [0x2F, 0x00, 0x1A, 0x00, 0x02, 0x00, 0x00, 0x00]

    # transmit.extend(header)
    # transmit.extend(data)

    # # enable tpdo
    # data = [0x23, 0x00, 0x18, 0x01, 0x81, 0x01, 0x00, 0x40]

    # transmit.extend(header)
    # transmit.extend(data)

    # # create TPDO
    # data = [0x23, 0x00, 0x18, 0x01, 0x81, 0x01, 0x00, 0x40]

    # transmit.extend(header)
    # transmit.extend(data)


    return transmit

data = setup_tpdo()
print(data)
data_bytes = bytes(data)
print(data_bytes)

TCP_IP_INV = '192.168.0.8'
TCP_PORT_CAN1 = 20001

print("opening socket")


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((TCP_IP_INV, TCP_PORT_CAN1))
print("socket connected")
while True:




   

    sock.send(data_bytes)

    print("data sent")

    #sock.close()

    time.sleep(1)