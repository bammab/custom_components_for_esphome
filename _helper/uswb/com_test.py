from crc import Calculator, Crc16
import struct
import serial
import logging
import time

logger = logging.getLogger(__name__)

START_MSG_FRAME = bytes([0x5A,0xA5])
MSG_LENGTH_BYTES = 1 # third byte hold the message length without SOF and length byte himself
MODE_MASTER = False
MODE_SLAVE_ID = 3
COM_PORT = "COM5"
MAX_CURRENT_A = 8

MODE_MASTER = False
MODE_SLAVE_ID = 2
COM_PORT = "COM7"

def main():
    setup_logger()
    logger.info("Logger setup successful")
    setup_communication(master=MODE_MASTER)

def setup_logger():
    global logger
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    # ch.setLevel(logging.DEBUG)
    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

def bytes_to_hexstring(bytes):
    return ' '.join(['0x{:02X}'.format(x) for x in bytes])

def calc_checksum_wb(data, with_crc=True):
    calculator = Calculator(Crc16.MODBUS)
    crc_expected = 0
    if with_crc:
        crc_expected = bytes(data[-2:])
        data = data[:-2]
    data = bytes(data)
    crc = calculator.checksum(data[-5:])
    crc_byte = struct.pack("<H", crc)
    # print(f"Check data {bytes_to_hexstring(data)} ({bytes_to_hexstring(crc_byte)}) -> {crc_expected == crc_byte}")
    return crc_byte

def setup_communication(master=True):
    with serial.Serial() as ser:
        ser.baudrate = 4800
        ser.port = COM_PORT
        ser.timeout = 1
        ser.open()
        # ser.write(b'hello')
        logger.info("Opened serial port")
        if master:
            handle_master_comm(ser)
        else:
            handle_client_comm(ser)

def handle_master_comm(ser: serial.Serial):
    logger.info("Start MASTER mode")
    allow_loading = True
    initial_current = 0
    initial_current = MAX_CURRENT_A
    allow_timeslot = 20
    while True:
        # TEST ONLY: change allowed current after a few seconds
        allow_timeslot -= 1
        if allow_timeslot <= 0:
            initial_current = 0
        # for i in range(2,10):
        for i in [MODE_SLAVE_ID]:
            logger.info(f"Send initial message to slave {i}")
            msg = START_MSG_FRAME + bytes([0x07, 0x00, i, 0x02, 0x01, initial_current])
            msg = msg + calc_checksum_wb(msg, False)
            ser.write(msg)
            logger.debug("-> send: " + bytes_to_hexstring(msg))
            time.sleep(0.05)
            if ser.in_waiting > 0:
                logger.debug("Serial port in readable state")
                response = ser.read(3)
                if (response[:2] == START_MSG_FRAME):
                    response += ser.read(response[2])
                    logger.debug("<- recv: " + bytes_to_hexstring(response))
                    if response[7] != 0:
                        logger.info(f"Slave wallbox {i} want to load with {response[7]}A - allow {initial_current}A")

        time.sleep(2)
    

def handle_client_comm(ser: serial.Serial):
    logger.info(f"Start SLAVE mode (id: {MODE_SLAVE_ID})")
    sof = False
    msg = b''
    load_count = 3 # simulate charging until Nth message from master arrived
    while True:
        c = ser.read()
        # logger.debug(f"Read byte {bytes_to_hexstring(c)}")
        if not sof and len(c) > 0 and (c[0] == START_MSG_FRAME[0]):
            msg = c
        elif not sof and len(msg) == 1 and c[0] == START_MSG_FRAME[1]:
            msg += c
            sof = True
        elif sof:
            msg += c
        elif len(c) > 0:
            logger.warning(f"Unknown state: '{bytes_to_hexstring(msg)}' and new byte {bytes_to_hexstring(c)}")
        else:
            continue

        # logger.debug(f"Current msg: {bytes_to_hexstring(msg)}")

        # Process msg
        # if len(msg) == 10:
        if len(msg) >= 3 and len(msg) == (len(START_MSG_FRAME) + MSG_LENGTH_BYTES + msg[2]):
            sof = False
            # logger.debug("<- recv: " + bytes_to_hexstring(msg))
            if msg[-2:] != calc_checksum_wb(msg):
                logger.warning("Checksum mismatch - ignore data")
                continue
            if msg[4] != MODE_SLAVE_ID:
            # if msg[4] != MODE_SLAVE_ID and msg[4] != MODE_SLAVE_ID + 1: # TEST ONLY: response to two slave ids
                # logger.debug(f"Ignore message - for another slave id ({msg[4]})")
                continue

            logger.debug("<- recv: " + bytes_to_hexstring(msg))
            # WANT_LOAD_A = 16 if msg[4] == MODE_SLAVE_ID else 0 # TEST ONLY: reponse different values if simulating two slaves
            load_count -= 1
            WANT_LOAD_A = 9 if load_count > 0 else 0
            if msg[5:7] == bytes([0x02,0x01]):
                logger.info(f"Got allowed current: {msg[7]}/{WANT_LOAD_A}")
                msg = START_MSG_FRAME + bytes([0x07, 0x00, msg[4], 0x02, 0x02, WANT_LOAD_A])
                msg = msg + calc_checksum_wb(msg, False)
                ser.write(msg)
                logger.debug("-> send: " + bytes_to_hexstring(msg))
            # elif msg[5:8] == bytes([0x02,0x01,0x00]):
            #     pass
            else:
                logger.critical(f"Got unknown message - SKIP")

            # Reset all
            msg = []


# data = [
#     [0x5A,0xA5,0x07,0x00,0x02,0x02,0x01,0x00,0x85,0xE8],
#     [0x5A,0xA5,0x07,0x00,0x03,0x02,0x01,0x00,0x84,0x14],
#     [0x5A,0xA5,0x07,0x00,0x04,0x02,0x01,0x00,0x85,0x60],
#     [0x5A,0xA5,0x07,0x00,0x05,0x02,0x01,0x00,0x84,0x9C],
#     [0x5A,0xA5,0x07,0x00,0x06,0x02,0x01,0x00,0x84,0xD8],
#     [0x5A,0xA5,0x07,0x00,0x07,0x02,0x01,0x00,0x85,0x24],
#     [0x5A,0xA5,0x07,0x00,0x08,0x02,0x01,0x00,0x86,0x30],
#     [0x5A,0xA5,0x07,0x00,0x09,0x02,0x01,0x00,0x87,0xCC]
# ]

def test():
    slave_id = 0x02
    def cmsg(master=True, load=0):
        msg = START_MSG_FRAME + bytes([0x07, 0x00, slave_id, 0x02, (0x01 if master else 0x02), load])
        return msg + calc_checksum_wb(msg, False)

    msgs = [
        (True, 0, "Master initial scan"),
        (False, 0, "Wallbox without vehicle"),
        (True, 0, "Master next loop"),
        (False, 16, "Wallbox request 16A"),
        (True, 9, "Master allow 9A"),
        (False, 16, "Wallbox request 16A"),
        (True, 9, "Master allow 9A"),
        (False, 0, "Wallbox is ready"),
        (True, 0, "Master allow requested 0A"),
        (False, 0, "Wallbox same response"),
    ]
    for m in msgs:
        print(f"{m[2]:<26}{'>>' if m[0] else '<<'} {bytes_to_hexstring(cmsg(m[0], m[1]))}")

if __name__ == '__main__':
    main()
    # test()
    
    # calculator = Calculator(Crc16.MODBUS)
    # data = bytes(b"\x00\x02\x02\x01\x00") #\x5A\xA5\x07\x00\x02\x02\x01\x00
    # # data = b'123456789'
    # crc = calculator.checksum(data)
    # crc_byte = struct.pack("<H", crc)
    # print(bytes_to_hexstring(crc_byte))
