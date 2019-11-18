import time
import serial


class IrSerialServices:
    @staticmethod
    def try_open_serial_connection(port):
        connection = None
        try:
            connection = serial.Serial(port, 9600, timeout=0)
            time.sleep(2.5)
        except Exception as e:
            print(f'unable to open serial port {port}, {str(e)}')
        return connection

    @staticmethod
    def try_move_and_start_capture(connection, degrees):
        print(degrees)
        try:
            assert 0 <= degrees <= 180, "bad degrees"
            start_letter = b'A'
            degrees_10 = (180 - degrees) / 10
            letter = bytes([start_letter[0] + int(degrees_10)])
            connection.write(letter)
            time.sleep(1.5)  # give the servo time to move
        except Exception as e:
            print(f'exception while trying to write to serial, {str(e)}')
            connection = None

    @staticmethod
    def try_stop_and_get_capture(connection):
        response = ''
        try:
            connection.write(b'Z')
            time.sleep(0.1)
            response = connection.read(1000)
        except Exception as e:
            print(f'exception while trying to write to serial, {str(e)}')
            connection = None
        return response

    @staticmethod
    def try_stop_and_search_response(connection, group=-1, device=-1, state=-1, temperature=-1):
        capture = IrSerialServices.try_stop_and_get_capture(connection)
        if connection is not None:
            inp = IrNecParser()
            if state == 0:
                temperature = -1
            return inp.is_ir_match(capture, group, device, state, temperature)
        return False


class IrNecParser:

    _reversed = [
        '0',   # 0000 -> 0000
        '8',   # 0001 -> 1000
        '4',   # 0010 -> 0100
        'c',   # 0011 -> 1100
        '2',   # 0100 -> 0010
        'a',   # 0101 -> 1010
        '6',   # 0110 -> 0110
        'e',   # 0111 -> 1110
        '1',   # 1000 -> 0001
        '9',   # 1001 -> 1001
        '5',   # 1010 -> 0101
        'd',   # 1011 -> 1101
        '3',   # 1100 -> 0011
        'b',   # 1101 -> 1011
        '7',   # 1110 -> 0111
        'f'    # 1111 -> 1111
    ]

    def __init__(self):
        self.group = 0
        self.device = 0
        self.state = 0
        self.temperature = 0

    def _parse(self, stream):
        # stream = byte_stream.decode('utf-8')
        if len(stream) == 7:
            stream = '0' + stream
        # print(stream)
        try:
            # sanity check
            if (int(stream[0], 16) == 15 - int(stream[2], 16)) and \
               (int(stream[1], 16) == 15 - int(stream[3], 16)) and \
               (int(stream[4], 16) == 15 - int(stream[6], 16)) and \
               (int(stream[5], 16) == 15 - int(stream[7], 16)):
                address = self._reversed[int(stream[1], 16)] + self._reversed[int(stream[0], 16)]
                data = self._reversed[int(stream[5], 16)] + self._reversed[int(stream[4], 16)]
                self.group = int(address, 16) & 0x1f
                self.device = (int(address, 16) & 0xe0) >> 5
                self.state = int(data, 16) & 0x1
                self.temperature = (int(data, 16) & 0x3e) >> 1
                return
        except Exception as e:
            print(f'Failed to parse IR message {stream}: {str(e)}')
        self.group = self.device = self.state = self.temperature = 0

    def is_ir_match(self, byte_stream, group=-1, device=-1, state=-1, temperature=-1):
        words = byte_stream.decode('utf-8').split(':')
        for word in words:
            current_match = True
            self._parse(word)
            if group != -1 and group != self.group:
                current_match = False
            if device != -1 and device != self.device:
                current_match = False
            if state != -1 and state != self.state:
                current_match = False
            if temperature != -1 and temperature != self.temperature:
                current_match = False
            if group != 0:
                print(word)
                print(f'room({group}/{self.group}), device({device}/{self.device}), ' +
                      f'state({state}/{self.state}), temperature({temperature}/{self.temperature})')
            if current_match:
                return True
        return False


if __name__ == "__main__":
    con1 = IrSerialServices.try_open_serial_connection('COM18')
    con2 = IrSerialServices.try_open_serial_connection('COM19')
    time.sleep(2)
    for deg in range(0,10):
        print(deg * 10)
