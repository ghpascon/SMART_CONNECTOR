from .on_receive import OnReceive
from .rfid import RfidCommands
from .serial_protocol import SerialProtocol

class X714(SerialProtocol, OnReceive, RfidCommands):
    def __init__(self, config, name):
        self.is_rfid_reader = True

        self.config = config
        self.port = self.config.get("CONNECTION")
        self.baudrate = self.config.get("BAUDRATE")
        self.vid = self.config.get("VID", 1)
        self.pid = self.config.get("PID", 1)
        self.name = name

        self.transport = None
        self.on_con_lost = None
        self.rx_buffer = bytearray()
        self.last_byte_time = None

        self.is_connected = False
        self.is_reading = False

        self.is_auto = self.port == "AUTO"


    def write(self, to_send, verbose=True):
        self.write_serial(to_send, verbose)

    async def connect(self):
        await self.connect_serial()