#! /usr/bin/python3

import os
import time
import random
from json import dumps
from httplib2 import Http
from subprocess import Popen, PIPE

def sprintf(format, *args):
    return format % args
#-------


class OpenVPN_Supervisor:
    #session_id
    #ovpn_ping_command
    #message_api_address

    def __init__(self, sid):
        if sid == None:
            sid = ""
            
        sid = sid.strip()
        
        if sid == "":
            sid = 'ovpn-supervisor-' + random.randint(10000, 99999)
        
        self.session_id = sid
        self.ovpn_ping_command = None
        self.message_api_address = None
    #-------
        
    def setPingAddress(self, ping_addr):
        if ping_addr == None:
            self.ovpn_ping_command = None
            
        ping_addr = ping_addr.strip()
        
        if ping_addr == "":
            self.ovpn_ping_command = None

        self.ovpn_ping_command = "ping -c 1 " + ping_addr
    #-------
    
    def setMessageAPIAddress(self, addr):
        if addr == None:
            self.message_api_address = None
            
        addr = addr.strip()
        
        if addr == "":
            self.message_api_address = None

        self.message_api_address = addr
    #-------

    def sendMessage(self, msg):
        if self.message_api_address == None or msg == None:
            return
            
        msg = msg.strip()
        
        if msg == "":
            return
            
        http_obj = Http()    
            
        res = http_obj.request(
            uri = self.message_api_address,
            method = 'POST',
            headers = {'Content-Type': 'application/json; charset=UTF-8'},
            body = dumps({'text': sprintf("%s :: %s", sid, msg)})
        )
        
        #print("Message API Responde: ")
        #print(res)
    #-------       
        
    def start(self):
        print("Starting OpenVPN")
    
        while True: # endless
            openvpn_proc = Popen(['/usr/sbin/openvpn-real', '--config', '/etc/openvpn/ovpn.conf'], stdout=PIPE, stderr=PIPE)
            time.sleep(4)

            while True:
                time.sleep(1)
                retcode = openvpn_proc.poll()
                
                if retcode is not None: # Process finished
                    print("OpenVPN process die - restarting")
                    self.sendMessage("restarting after openvpn die")
                    time.sleep(2)
                    break
                    
                # OpenVPN still work (good)
                
                if self.ovpn_ping_command is not None:
                    ping_responde = os.system(self.ovpn_ping_command)

                    if ping_responde != 0: # Ping fail
                        print("OpenVPN ping fail - restarting")
                        self.sendMessage("restarting after ping fail")
                        openvpn_proc.terminate()
                        time.sleep(2)
                        break

                #continue
    #-------
    
#-------


sid = os.getenv('OVPN_SUPERVISOR_SID')
msg_api_address = os.getenv('OVPN_MESSAGE_API_ADDRESS')
ovpn_server_ip = "10.8.0.1"


ovpn_sv = OpenVPN_Supervisor(sid)
ovpn_sv.setPingAddress(ovpn_server_ip)
ovpn_sv.setMessageAPIAddress(msg_api_address)
ovpn_sv.start()


