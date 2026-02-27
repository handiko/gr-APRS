import numpy as np
from gnuradio import gr
import pmt
import socket
import threading
import time

class blk(gr.sync_block):
    def __init__(self, callsign='N0CALL', passcode='-1', 
                 lat='0000.00N', lon='00000.00E', 
                 comment='GNU Radio I-Gate',
                 beacon_interval=600, 
                 server='rotate.aprs.net', port=14580):
        
        gr.sync_block.__init__(self, name='APRS-IS I-Gate', in_sig=None, out_sig=None)
        
        # Parameters
        self.callsign = callsign
        self.passcode = passcode
        self.lat = lat  
        self.lon = lon  
        self.comment = comment # New user-configurable comment
        self.beacon_interval = beacon_interval
        self.server = server
        self.port = port
        
        # Internal State
        self.sock = None
        self.connected = False
        self.running = True

        # Message Port
        self.message_port_register_in(pmt.intern('pdu_in'))
        self.set_msg_handler(pmt.intern('pdu_in'), self.handle_msg)

        # Start Networking Thread
        self.net_thread = threading.Thread(target=self.network_loop)
        self.net_thread.daemon = True
        self.net_thread.start()

    def connect(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(10)
            self.sock.connect((self.server, self.port))
            # Login String
            login = f"user {self.callsign} pass {self.passcode} vers GRC-IGate 1.1\r\n"
            self.sock.sendall(login.encode('ascii'))
            self.connected = True
            print(f"[I-Gate] Connected to {self.server} as {self.callsign}")
        except Exception as e:
            print(f"[I-Gate] Connection failed: {e}")
            self.connected = False

    def network_loop(self):
        last_beacon = 0
        while self.running:
            if not self.connected:
                self.connect()
                time.sleep(15) 
                continue
            
            now = time.time()
            if (now - last_beacon) > self.beacon_interval:
                # APRS Position Report: !Lat/Lon&Comment
                # '!' is the Data Type ID
                # '/' is the Symbol Table ID
                # '&' is the Symbol Code (Map icon for I-Gate)
                beacon_pkt = f"{self.callsign}>APRS,TCPIP*:!{self.lat}/{self.lon}&{self.comment}\r\n"
                self.send_to_aprs(beacon_pkt)
                last_beacon = now
            
            time.sleep(1)

    def send_to_aprs(self, packet_str):
        if self.connected and self.sock:
            try:
                self.sock.sendall(packet_str.encode('ascii'))
            except:
                self.connected = False
                print("[I-Gate] Connection lost. Attempting reconnect...")

    def handle_msg(self, msg_pmt):
        try:
            msg_py = pmt.to_python(msg_pmt)
            # Handle both PMT pairs (PDU) and strings
            if isinstance(msg_py, tuple):
                raw_str = "".join(map(chr, msg_py[1]))
            else:
                raw_str = str(msg_py)

            # Extract TNC2 data
            if "AX.25 Frame: " in raw_str:
                tnc2_data = raw_str.split("AX.25 Frame: ")[1].strip()
            else:
                tnc2_data = raw_str.strip()

            if tnc2_data and ":" in tnc2_data:
                header, payload = tnc2_data.split(":", 1)
                # Inject I-Gate path (qAR) and forward to APRS-IS
                formatted_pkt = f"{header},qAR,{self.callsign}:{payload}\r\n"
                self.send_to_aprs(formatted_pkt)
                    
        except Exception as e:
            # Silently ignore malformed frames to keep the console clean
            pass

    def stop(self):
        self.running = False
        if self.sock:
            self.sock.close()
        return True