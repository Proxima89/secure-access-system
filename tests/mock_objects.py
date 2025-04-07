from unittest.mock import MagicMock

#Mocks the GPIO module
class MockGPIO:
    BCM = 1
    OUT = 1
    LOW = 0
    HIGH = 1
    
    @staticmethod
    def setmode(mode):
        pass
    
    @staticmethod
    def setup(pin, mode):
        pass
    
    @staticmethod
    def output(pin, value):
        pass
    
    @staticmethod
    def cleanup():
        pass

#Mocks the SMBus module
class MockSMBus:
    def __init__(self, bus):
        self.write_byte = MagicMock()
    
    #Mocks the write_byte method
    def write_byte(self, addr, data):
        pass

#Mocks the SimpleMFRC522 module
class MockSimpleMFRC522:
    def __init__(self):
        pass
    
    def read(self):
        return (12345, "Test User")