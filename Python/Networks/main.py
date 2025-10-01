'''
Scope: simulate client server architecture 
'''
from abc import ABC, abstractmethod

class RouterSender:
    pass

class RouterReciever:
    pass

class Client:
    pass

class Server:
    pass

class PDU(ABC):
    # protocol data unit ---> interface
    pass

class Datagram(PDU):
    pass

class Segment(Datagram):
    pass

class Packet(Segment):
    pass

class Frames(Packet):
    pass

