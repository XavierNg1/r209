# -*- coding: utf-8 -*-
from twisted.internet.protocol import DatagramProtocol
from c2w.main.lossy_transport import LossyTransport
import logging
import struct
from twisted.internet import reactor
#sequence_number


logging.basicConfig()
moduleLogger = logging.getLogger('c2w.protocol.udp_chat_server_protocol')


class c2wUdpChatServerProtocol(DatagramProtocol):

    def __init__(self, serverProxy, lossPr):
        """
        :param serverProxy: The serverProxy, which the protocol must use
            to interact with the user and movie store (i.e., the list of users
            and movies) in the server.
        :param lossPr: The packet loss probability for outgoing packets.  Do
            not modify this value!

        Class implementing the UDP version of the client protocol.

        .. note::
            You must write the implementation of this class.

        Each instance must have at least the following attribute:

        .. attribute:: serverProxy

            The serverProxy, which the protocol must use
            to interact with the user and movie store in the server.

        .. attribute:: lossPr

            The packet loss probability for outgoing packets.  Do
            not modify this value!  (It is used by startProtocol.)

        .. note::
            You must add attributes and methods to this class in order
            to have a working and complete implementation of the c2w
            protocol.
        """
        #: The serverProxy, which the protocol must use
        #: to interact with the server (to access the movie list and to 
        #: access and modify the user list).
        self.serverProxy = serverProxy
        self.lossPr = lossPr
        self.num_sequence=0

    def startProtocol(self):
        """
        DO NOT MODIFY THE FIRST TWO LINES OF THIS METHOD!!

        If in doubt, do not add anything to this method.  Just ignore it.
        It is used to randomly drop outgoing packets if the -l
        command line option is used.
        """
        self.transport = LossyTransport(self.transport, self.lossPr)
        DatagramProtocol.transport = self.transport


    def datagramReceived(self, datagram, host_port):
        """
        :param string datagram: the payload of the UDP packet.
        :param host_port: a touple containing the source IP address and port.
        
        Twisted calls this method when the server has received a UDP
        packet.  You cannot change the signature of this method.
        """
        #Receiving the login request
        msg_length = struct.unpack('!H', datagram[0:2])[0]
        num_seq_and_type = struct.unpack('!H', datagram[2:4])[0]
        num_seq_msg = num_seq_and_type >> 4
        connection_type = num_seq_and_type & 15
        msg = struct.unpack(str(len(datagram[4:]))+'s', datagram[4:])[0].decode('utf-8')
        print(connection_type)
        print(num_seq_msg)
        print(msg)
        
        #sending the ACK message
        num_seq = 0
        num_seq = num_seq << 4
        ack_type = 0
        seq_and_ack = num_seq + ack_type
        ack_length = 4
        buf = struct.pack('!hh', ack_length, seq_and_ack)
        #self.transport.connect(host_port[0], host_port[1])
        #self.transport.write(answer.encode('utf-8'))
        self.transport.write(buf, (host_port[0], host_port[1]))

        #sending the connection message
        num_seq = 0
        num_seq = num_seq << 4
        connection_type = 7
        seq_and_ack = num_seq + connection_type
        ack_length = 4
        buf = struct.pack('!hh', ack_length, seq_and_ack)
        #self.transport.connect(host_port[0], host_port[1])
        #self.transport.write(answer.encode('utf-8'))
        self.transport.write(buf, (host_port[0], host_port[1]))
       
        
        pass
