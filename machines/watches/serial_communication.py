import serial


class Serial:
    PORT = 'COM3'
    TIMEOUT = 0

    def __init__(self):
        self.ser = serial.Serial(self.PORT, 115200, timeout=self.TIMEOUT)

    def send(self, byte_string):
        self.ser.write(byte_string)

    def encase_and_send(self, code, data=b''):
        """add '<' and '>' as start and end of message and also code to identify message type
        codes:
            \x01 - start communication(and turn off QR code)
            \x02 - end communication
            \x03 - pass data
        """

        start = b'<'
        end = b'>'
        self.send(b''.join((start, code, data, end)))

    def send_start(self):
        self.encase_and_send(b'\x01')

    def send_end(self):
        self.encase_and_send(b'\x02')

    def send_positions(self, data):
        # data is an array of positions of revolute joints in interval [0; 255]
        self.encase_and_send(b'x03', bytearray(data))
