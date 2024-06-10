
import glob, serial, re

class Machine:
    def __init__(self):
        self.loaded = None
        self.ser = None

        self._bootCommands = [
            "G90",
            "M260 A112 B1 S1",
            "M260 A109",
            "M260 B48",
            "M260 B27",
            "M260 S1",
            "M260 A112 B2 S1",
            "M260 A109",
            "M260 B48",
            "M260 B27",
            "M260 S1",
            "G0 F35000"
        ]

        if not self.findPort():
            print("could not find serial port!")


    def goto(self, x=None, y=None, z=None):
        command = "G0"
        if x is not None:
            command = command + " X" + str(x)
        if y is not None:
            command = command + " Y" + str(y)
        if z is not None:
            command = command + " Z" + str(z)

        self.send(command)

    def safeZ(self):
        self.send("G0 Z31.5")

    def home(self):
        self.send("G28 X")
        self.send("G28 Y")
        self.send("G28")

    def pump(self, value):
        if value:
            self.send("M106")
            self.send("M106 P1 S255")
        else:
            self.send("M107 P1")
            self.send("M107")

    def findPort(self):
        # checks for valid serial ports and opens ser object to the first one found
        ports = glob.glob('/dev/cu.usb*')
        for port in ports:
            try:
                self.ser = serial.Serial(port, timeout=100)
                for i in self._bootCommands:
                    self.send(i)
                return True
            except (OSError, serial.SerialException):
                return False
            
    def send(self, command):
        self.ser.reset_input_buffer()
        encoded = command.encode('utf-8')
        self.ser.write(encoded + b'\n')
        resp = self.ser.readline().decode('ISO-8859-1')
        #print(str(resp))
        return resp

    def park(self):
        self.goto(x=218, y=430)

    def readLeftVac(self): # returns vacuum sensor value for left vac

        try:
            #selects vac 1 through multiplexer
            self.send("M260 A112 B1 S1")

            #read addresses 0x06 0x07 and 0x08 for pressure reading
            self.send("M260 A109 B6 S1")
            msb = re.search("data:(..)", self.send("M261 A109 B1 S1"))

            self.send("M260 A109 B7 S1")
            csb = re.search("data:(..)", self.send("M261 A109 B1 S1"))

            self.send("M260 A109 B8 S1")
            lsb = re.search("data:(..)", self.send("M261 A109 B1 S1"))

            val = msb.group(1)+csb.group(1)+lsb.group(1)

            result = int(val, 16)

            if(result & (1 << 23)):
                result = result - 2**24

            return result
        except Exception as e: 
            print(e)
            return False
      