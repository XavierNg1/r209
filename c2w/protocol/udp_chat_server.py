# -*- coding: utf-8 -*-
from twisted.internet.protocol import DatagramProtocol
from c2w.main.lossy_transport import LossyTransport
import c2w.protocol.util as util
import logging
import struct
from twisted.internet import reactor
from c2w.main.constants import ROOM_IDS


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
        self.usersList=[]
        #self.movies=[]
        self.filattente=[]
        self.username=""
        
    # fonction pour verifier si on a recu un ack
    def traitementAck(self,numSeq,host_port): 	 
        for p in self.filattente:             	 
            if (p[4]==host_port):
                if (p[0]==numSeq):
                    p[2]=1
                    #print(p[0]) 
                    self.num_sequence+=1
                    print(self.num_sequence)
                    #self.filattente.remove(p)
                    print('ack envoye par le client')    

    #pass

	#fonction pour envoyer le paquet si jamais on a toujours pas recu d ack
    def sendAndWaite(self,host_port):   
        for p in self.filattente:
            if (p[4]==host_port):             	 
                if (p[1] <=7):#remission
                    if (p[2] == 0):
                        self.transport.write(p[3],p[4])
                        p[1]+=1
                        print('nombre de message envoye:'+str(p[1]))
                        reactor.callLater(1,self.sendAndWaite,p[4])
                        #reactor.run()
                    elif(p[2] == 1):
                        print('avant',self.filattente)
                        print('Le paquet a ete aquitte',p[0])  
                        self.filattente.remove(p)
                        #self.num_sequence+=1
                        print("Dernier num sequnce",self.num_sequence)
                        print('apres',self.filattente) #reactor.callLater(0,self.sendAndWaite, (host_port[0], host_port[1]) ))

                        """"
                        if self.num_sequence==1:
                            print("********************************ENVOIE LISTE DES FILM**************************")
                            #self.num_sequence=1
                            # print(util.format_moviesList(self.serverProxy.getMovieList()))
                            listMovie=util.format_moviesList(self.serverProxy.getMovieList())
                            print(util.get_moviesList(util.format_moviesList(self.serverProxy.getMovieList())))
                            self.filattente.append([1,1,0,listMovie,(host_port[0], host_port[1])])
                            self.transport.write(listMovie, (host_port[0], host_port[1]))
                            reactor.callLater(1,self.sendAndWaite, (host_port[0], host_port[1]) )
                        """

                        #print('apres',self.filattente) #reactor.callLater(0,self.sendAndWaite, (host_port[0], host_port[1]) ))
        #return self.num_sequence
    #pass

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

       # if is not (firstconnection):
        for user in self.usersList:
            if (user[1]==host_port):
                self.num_sequence=user[4]
            else:
                self.num_sequence=0

                

        packet_type=util.get_type(datagram)
        num_sequence_client=util.get_numSequence(datagram)
        if packet_type ==0:  #Reception ACK

            self.traitementAck(num_sequence_client,host_port)     
            #self.num_sequence+=1      

            if self.num_sequence==1:
                
                
                
                #self.serverProxy.addUser(userName,ROOM_IDS.MAIN_ROOM,None,host_port)
                

                print("********************************ENVOIE LISTE DES FILM**************************")
                #self.num_sequence=1
                # print(util.format_moviesList(self.serverProxy.getMovieList()))
                listMovie=util.format_moviesList(self.serverProxy.getMovieList())
                print(util.get_moviesList(util.format_moviesList(self.serverProxy.getMovieList())))
                self.filattente.append([1,1,0,listMovie,(host_port[0], host_port[1])])
                self.transport.write(listMovie, (host_port[0], host_port[1]))
                reactor.callLater(1,self.sendAndWaite, (host_port[0], host_port[1]) )

            
            elif self.num_sequence==2:
                print("********************************ENVOIE LISTE DES USER**************************")
                print(util.format_usersList(self.usersList,self.serverProxy.getMovieList()))
                listUser=util.format_usersList(self.usersList,self.serverProxy.getMovieList())
                #self.filattente.append([2,1,0,listUser,(host_port[0], host_port[1])])
                
                
                for user in self.usersList:
                    self.transport.write(listUser, (user[1][0], user[1][1]))
                    self.filattente.append([user[4],1,0,listUser,(user[1][0], user[1][1])])####AJOUTER POUR TESTER LA RETANSMISSION DE LA LIST DES USER
                    reactor.callLater(1,self.sendAndWaite, (user[1][0], user[1][1]) )
                

                #self.transport.write(listUser, (host_port[0], host_port[1]))
                
                
                
                #reactor.callLater(1,self.sendAndWaite, (host_port[0], host_port[1]) )
                
                print(util.get_usersList(listUser,util.get_moviesList(util.format_moviesList(self.serverProxy.getMovieList()))))
          #  print(packet_type)
            
        elif packet_type ==1:  # Reception login request 
            
            pseudo=True
            userName=util.get_userName_connection(datagram)
            for user in self.usersList:
                
                if userName==user[0]:
                    pseudo=False
            
            
            if pseudo==True:
                iDUser=self.serverProxy.addUser(userName,ROOM_IDS.MAIN_ROOM,None,host_port) #retounre l'ID du client

                iDRoom=0
                nameRoom="Main Room"
                num_sequence_Server=0
                self.usersList.append([userName,host_port,nameRoom,iDRoom,num_sequence_Server]) #le second 0 esl l'ID de MainROOM
                #self.usersList.append(['test'+userName,host_port,'Big Buck Bunny',2,num_sequence_Server])
                #self.usersList.append(['test2'+userName,host_port,'Sintel - Trailer',3,num_sequence_Server])
                print("*****************LA LIST DES USERS")
                print(self.usersList)
                print(self.serverProxy.getUserList()[0].userChatRoom)
                print(self.serverProxy.getUserList())
                print("oooooooooooooooooooooooooooooooooooo")
                print("******^^^^^^^^^^^^^^**********")
                print(iDUser)
                print("******^^^^^^^^^^^^^^**********")

                # print(self.serverProxy.getMovieList()[0])
                
                """
                Traitement a effectuer !!!
                """

                #sending the ACK message
                buf=util.format_ack(num_sequence_client)
                
                self.transport.write(buf, (host_port[0], host_port[1]))


                #sending the connection message
                #num_seq = 0
                #num_seq = num_seq << 4
                #connection_type = 7
                #seq_and_ack = num_seq + connection_type
                #ack_length = 4
                #buf = struct.pack('!hh', ack_length, seq_and_ack)
                #self.transport.connect(host_port[0], host_port[1])
                #self.transport.write(answer.encode('utf-8'))

                buf2=util.format_header(7,self.num_sequence)
                self.transport.write(buf2, (host_port[0], host_port[1]))
                self.filattente.append([self.num_sequence,1,0,buf2,(host_port[0], host_port[1])])
                print("**********",self.num_sequence)
                reactor.callLater(1,self.sendAndWaite, (host_port[0], host_port[1]) )
                #reactor.callLater(1,print,self.num_sequence)
                #reactor.run()
                #reactor.stop
                #""" DECOMMENTER POUR FAIRE FONCTIONNER LE TEST MOVIELIST
                
                #reactor.callLater(1,self.sendAndWaite, (host_port[0], host_port[1]) )

                #"""
                    

                #reactor.callLater(1,self.sendAndWaite, (host_port[0], host_port[1]) )

                
                #   print('test',self.filattente)
                    
                #   print('avant',self.filattente)
                    #self.transport.write(buf2, (host_port[0], host_port[1]))
                    
                    #reactor.run()
                
                """
                Test du Usernanme
                """

            elif pseudo==False:
                buf=util.format_ack(num_sequence_client)

                self.transport.write(buf, (host_port[0], host_port[1]))


                buf2=util.format_header(8,self.num_sequence)
                self.transport.write(buf2, (host_port[0], host_port[1]))
                self.filattente.append([self.num_sequence,1,0,buf2,(host_port[0], host_port[1])])#jai mi 1 pour voir
                #print("**********",self.num_sequence)
                reactor.callLater(1,self.sendAndWaite, (host_port[0], host_port[1]) )

        

                """
                elif packet_type ==2:  # Quitter Application 
                    print("jeveuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuupannnnnnnnnnnn")
                    buf=util.format_ack(num_sequence_client)
                    print("jeveuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuupannnnnnnnnnnn")
                    self.transport.write(buf, (host_port[0], host_port[1]))
                    print("jeveuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuupannnnnnnnnnnn")
                    
                
                    for user in self.usersList:
                        print("rttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt")
                        if user[1]==host_port:
                            self.usersList.remove(user)
                            print("/***********************************USER A SUPRIMER",user[0])
                            self.serverProxy.removeUser(user[0])
                    


                    if self.usersList!=[]:
                        listUser=util.format_usersList(self.usersList,self.serverProxy.getMovieList())
                        for user in self.usersList:
                            self.transport.write(listUser, (user[1][0], user[1][1]))
                            reactor.callLater(user[4],self.sendAndWaite, (user[1][0], user[1][1]) )

                """

        
        
        elif packet_type == 3: # Choix de film
            #self.users.append(self.username)
            print(packet_type)
         

        elif packet_type==4: #
            t=0   
        elif packet_type==9:  # rdd
            t=0
        """    
        #Receiving the login request
        msg_length = struct.unpack('!H', datagram[0:2])[0]
        num_seq_and_type = struct.unpack('!H', datagram[2:4])[0]
        num_seq_msg = num_seq_and_type >> 4
        connection_type = num_seq_and_type & 15
        userName = struct.unpack(str(len(datagram[4:]))+'s', datagram[4:])[0].decode('utf-8')
        print(connection_type)
        print(num_seq_msg)
        #print(self.serverProxy.getMovieList())

        print(userName)
        #print(self.serverProxy.getMovieList())
                
        #self.serverProxy.addUser(userName,ROOM_IDS.MAIN_ROOM,None,host_port)  
        
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
        
        #print(ROOM_IDS.MAIN_ROOM)  
        
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

        self.transport.write(buf, (host_port[0], host_port[1]))
       """
        
        for user in self.usersList:
            if (user[1]==host_port):
                user[4]=self.num_sequence
                print(user[0])
                print("-------------------------------------------------------------------")
                print(user[4])
                print(self.num_sequence)

           

        pass
