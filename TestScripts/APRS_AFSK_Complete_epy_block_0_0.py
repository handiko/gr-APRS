import numpy as np
from gnuradio import gr
import pmt
import struct
from datetime import datetime

# --- AX.25 SUPPORT CLASSES AND FUNCTIONS ---

class AX25Address(object):
    def __init__(self):
        self.callsign = None
        self.ssid = None
        self.ch_bit = None
        self.reserved = None

    def __str__(self):
        if self.ssid == 0:
            return self.callsign
        else:
            return f"{self.callsign}-{self.ssid}"

    def to_bytes(self, last_addr=False, ch_bit=None):
        if self.callsign is None or not isinstance(self.ssid, int):
            raise ValueError("Address fields not populated!")
        padded_cs = f"{self.callsign:<6}"
        array = bytearray([ord(c) << 1 for c in padded_cs])
        last_byte = self.ssid << 1
        if last_addr: last_byte |= 1
        if (ch_bit is None and self.ch_bit) or ch_bit: last_byte |= 0x80
        array.append(last_byte)
        return array

class AX25Packet(object):
    def __init__(self):
        self.dest = None
        self.src = None
        self.digipeaters = []
        self.control = None
        self.frame_type = None
        self.protocol_id = None
        self.info = None

def bytes_to_address(array):
    addr = AX25Address()
    addr.callsign = ''.join([chr(d >> 1) for d in array[0:6]]).strip()
    addr.ssid = (array[6] >> 1) & 0x0f
    last = True if (array[6] & 0x01) else False
    return (last, addr)

def from_bytes(array):
    if len(array) < 15:
        raise ValueError("Packet too short")
    packet = AX25Packet()
    (last, packet.dest) = bytes_to_address(array[0:7])
    (last, packet.src) = bytes_to_address(array[7:14])
    offset = 14
    while not last:
        (last, addr_obj) = bytes_to_address(array[offset:offset+7])
        packet.digipeaters.append(addr_obj)
        offset += 7
    packet.control = array[offset]
    offset += 1
    # Check for UI frame or I frame which have protocol IDs
    if (packet.control & 0x03) == 0x03 or (packet.control & 0x01) == 0x00:
        packet.protocol_id = array[offset]
        offset += 1
    packet.info = array[offset:]
    return packet

def dump_packet(packet):
    ret = f"{packet.src}>{packet.dest}"
    for station in packet.digipeaters:
        ret += f",{station}"
    # Use latin-1 to preserve binary APRS data/symbols
    info_str = packet.info.decode('latin-1', errors='replace')
    ret += f":{info_str}"
    return ret

# --- GNU RADIO BLOCK ---

class blk(gr.sync_block):
    def __init__(self):
        gr.sync_block.__init__(self, name="HDLC to AX.25", in_sig=None, out_sig=None)
        self.message_port_register_in(pmt.intern('hdlc in'))
        self.message_port_register_out(pmt.intern('ax25 out'))
        self.set_msg_handler(pmt.intern('hdlc in'), self.handle_msg)

    def handle_msg(self, msg_pmt):
        msg_py = pmt.to_python(msg_pmt)
        if not isinstance(msg_py, tuple) or len(msg_py) < 2:
            return
        
        # Extract data from PDU (dict . vector)
        msg_data = bytearray(msg_py[1])

        try:
            pkt = from_bytes(msg_data)
            out_str = dump_packet(pkt)
            
            # 1. Print directly to GRC Console for easy reading
            print(f"AX.25 Frame: {out_str}")
            
            # 2. Send as PDU to next block (with newline for logging)
            pdu_str = out_str + '\n'
            out_data = np.array([ord(c) for c in pdu_str], dtype=np.uint8)
            self.message_port_pub(
                pmt.intern('ax25 out'), 
                pmt.cons(pmt.make_dict(), pmt.init_u8vector(len(out_data), out_data))
            )
                
        except Exception as e:
            # Uncomment for debugging parser errors:
            # print(f"Parser Error: {e}")
            pass

    def work(self, input_items, output_items):
        return 0