# -*- coding: utf-8 -*-
import struct

def prepare_header(numSeq,code_type):
        return (numSeq << 4 )+ code_type
 

def format_ack(num_sequence):
        num_seq = num_sequence << 4
        ack_type = 0
        seq_and_ack = num_seq + ack_type
        ack_length = 4
        packet = struct.pack('!hh', ack_length, seq_and_ack)
        return packet

def format_header(header_type,num_sequence):
        num_seq = num_sequence << 4
        seq_and_ack = num_seq + header_type
        ack_length = 4
        packet = struct.pack('!hh', ack_length, seq_and_ack)
        return packet

def format_login(userName):
        num_sequence , connection_type = 0,1
        num_seq = num_sequence << 4 
        packet_length = 4 + len(userName.encode('utf-8'))
        seq_and_connection = num_seq + connection_type
        length_username = str(len(userName))
        packet = struct.pack('!hh'+length_username+'s', packet_length, seq_and_connection, userName.encode('utf-8'))
        return packet

def get_userName_connection(packet):
        msg = struct.unpack(str(len(packet[4:]))+'s', packet[4:])[0].decode('utf-8')
        return msg 

def format_packet(numSeq,code_type,msgToSend):
        num_seq = numSeq<< 4 
        connection_type = code_type
        packet_length = 4 + len(msgToSend.encode('utf-8'))
        seq_and_connection = num_seq + connection_type
        length_username = str(len(msgToSend))
        packet = struct.pack('!hh'+length_username+'s', packet_length, seq_and_connection, msgToSend.encode('utf-8'))
        return packet

def format_chat(numSeq,code_type,userName,msgChat):
        num_seq = numSeq<< 4 
        connection_type = code_type
        packet_length = 4 + 1 + len(userName.encode('utf-8')) + len(msgChat.encode('utf-8'))
        userName_length = len(userName.encode('utf-8'))
        seq_and_connection = num_seq + connection_type
        length_msgChat = str(len(msgChat))
        length_username = str(len(userName))
        packet = struct.pack('!hhb'+length_username+'s'+length_msgChat+'s', packet_length, seq_and_connection, userName_length, userName.encode('utf-8'), msgChat.encode('utf-8'))
        return packet

def get_msgChat(packet):
        lenght=get_userName_length(packet)
        msg = struct.unpack(str(len(packet[5+lenght:]))+'s', packet[5+lenght:])[0].decode('utf-8')
        return msg 

def get_userName_fromChat(packet):
        lenght=get_userName_length(packet)
        userName = struct.unpack(str(len(packet[5:5+lenght]))+'s', packet[5:5+lenght])[0].decode('utf-8')
        return userName

def get_userName_length(packet):
        pseudo_length = struct.unpack('s', packet[4:5])[0].decode('utf-8')
        return pseudo_length 

def get_type(packet):
        num_seq_and_type = struct.unpack('!H', packet[2:4])[0]       
        code_type = num_seq_and_type & 15
        return code_type

def get_numSequence(packet):
        num_seq_and_type = struct.unpack('!H', packet[2:4])[0]
        numSeq = num_seq_and_type >> 4
        return numSeq

def get_packet_lenght(packet):
        packet_length = struct.unpack('!H', packet[0:2])[0]
        return packet_length


def get_users_list(packet):

        return 0


def send_Wait(packet, num_sequence):
        
        return 0


