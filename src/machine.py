
import glob, serial

class Machine:
    def __init__(self):
        self.loaded = None
        self.ser = None

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
        self.send("G28")

    def pump(self, value):
        if value:
            self.send("M106 P0 S255")
        else:
            self.send("M107 P0")

    def findPort(self):
        # checks for valid serial ports and opens ser object to the first one found
        ports = glob.glob('/dev/cu.usb*')
        for port in ports:
            try:
                self.ser = serial.Serial(port, timeout=100)
                return True
            except (OSError, serial.SerialException):
                return False
            
    def send(self, command):
        encoded = command.encode('utf-8')
        self.ser.write(encoded + b'\n')
        resp = self.ser.readline().decode('ISO-8859-1')
        print(str(resp))
      