# this module will be imported in the into your flowgraph

from datetime import datetime
import struct

'''
A library of functions and objects for manipulating AX.25 packets.
At the moment, it was mostly designed to handle APRS UI frames, so
further functionality has not been tested.
'''

class AX25Address(object):
    '''
    An object representing an AX.25 address. You can print this object to
    the screen, or cast it to a string.

    If the SSID is zero, the callsign will print as 'XXdYYY'. Otherwise,
    the SSID will appear as '-%d' at the end.
    '''
    def __init__(self):
        self.callsign = None
        self.ssid = None
        self.ch_bit = None
        self.reserved = None

    def __str__(self):
        if self.ssid == 0:
            return self.callsign
        else:
            return '%s-%d' % (self.callsign, self.ssid)

    def __repr__(self):
        return '<AX25Address(callsign=%s, ssid=%d)>' % (self.callsign,
                self.ssid)

    def to_bytes(self, last_addr=False, ch_bit=None):
        if (
                self.callsign is None
                or not isinstance(self.ssid, int)
           ):
            raise ValueError("Address fields not populated!")

        # Pad callsign with spaces to 6 chars
        padded_cs = '%-6s' % self.callsign

        array = bytearray([ord(c) << 1 for c in padded_cs])

        last_byte = self.ssid << 1

        if last_addr:
            last_byte |= 1

        if (ch_bit is None and self.ch_bit) or ch_bit:
            last_byte |= 0x80

        array.append(last_byte)
        return array

class AX25Packet(object):
    '''
    An object representing an AX.25 packet.
    '''
    def __init__(self):
        self.dest = None
        self.src = None
        self.digipeaters = []
        self.control = None
        self.frame_type = None
        self.recv_seq = None
        self.pf_bit = None
        self.send_seq = None
        self.supervisory_bits = None
        self.unnumbered_fm_bits = None
        self.protocol_id = None
        self.info = None
        self.timestamp = datetime.now()

    def __repr__(self):
        return '<AX25Packet(src=%s, dest=%s, frame_type=%s, len=%d)>' % \
                (self.src, self.dest, self.frame_type, len(self.info))

    def to_bytes(self):
        array = bytearray()
        array += self.dest.to_bytes()
        array += self.src.to_bytes(last_addr=(len(self.digipeaters) == 0))
        
        for i, dptr in enumerate(self.digipeaters):
            array += dptr.to_bytes(last_addr=(len(self.digipeaters) == (i+1)))

        # TODO: Handle various build conditions
        array += bytearray([self.control, self.protocol_id])
        array += bytearray(self.info)

        return array

    def kiss_wrap(self):
        return kiss_wrap_bytes(self.to_bytes())

    def checksum(self):
        ''' With thanks to W6KWF's excellent whitepaper '''
        crc = 0xffff

        for byte in self.to_bytes():
            # Byte to bits: bin returns 0bXXXXXXX
            bits = bin(byte)[2:].zfill(8)

            # Walk through bits (as string) backwards
            for i in xrange(7, -1, -1):
                bit = 1 if bits[i] == '1' else 0
                if (crc & 0x0001) != bit:
                    crc = (crc >> 1) ^ 0x8408
                else:
                    crc = crc >> 1

        return bytearray(struct.pack('<H', (crc ^ 0xffff)))

    def hdlc_wrap(self, preamble_count=1, trailer_count=1):
        out = ''
        pkt = self.to_bytes()
        csum = self.checksum()

        # Bytes to bits (LSB first)
        for byte in (pkt + csum):
            # bin() outputs 0bxxxxx, msb first
            # - strip off the 0b (using [2:])
            # - zero pad out to 8 bits (using .zfill)
            # - reverse string to be LSB first (with [::-1])
            out += bin(byte)[2:].zfill(8)[::-1]

        # Bit stuffing
        unstuffed = out
        stuffed = ''
        
        one_count = 0
        for bit in unstuffed:
            stuffed += bit

            # Keep a count of the number of subsequent 1's in a row
            if bit == '1':
                one_count += 1
            else:
                one_count = 0

            # If we hit 5 1's in a row, stuff a bit, and clear the counter
            if one_count == 5:
                stuffed += '0'
                one_count = 0

        out = stuffed

        # Preamble
        out = ('1111110' * preamble_count) + out
        out += ('0111111' * trailer_count)

        # Invert data, differentially encode
        out = [1 if c == '0' else 0 for c in out]
        for i in xrange(1, len(out) - 1):
            out[i] = out[i] ^ out[i-1]

        return out

def kiss_wrap_bytes(array):
    out = bytearray()
    out.append(0xc0)
    out.append(0x00)
    
    for bite in array:
        if bite == 0xc0:
            out.append(0xdb)
            out.append(0xdc)
        elif bite == 0xdb:
            out.append(0xdb)
            out.append(0xdd)
        else:
            out.append(bite)

    out.append(0xc0)

    return out

def bytes_to_address(array):
    ''' Converts an array of 7 bytes into an AX25Address object '''
    addr = AX25Address()
    addr.callsign = ''.join([chr(d >> 1) for d in array[0:6]]).strip()
    addr.ssid = (array[6] >> 1) & 0x0f
    addr.reserved = (array[6] >> 5) & 0x03
    addr.ch_bit = (array[6] >> 7) & 0x01

    last = True if (array[6] & 0x01) else False
    
    return (last, addr)

def string_to_address(string):
    ''' Converts a string (like "KB3VOZ -2") into an Address object '''
    if '-' in string:
        try:
            (cs, ssid) = string.split('-')
            ssid = int(ssid)
        except ValueError:
            raise ValueError("Bad callsign format")
    else:
        cs = string
        ssid = 0

    if len(cs) == 0 or len(cs) > 6 or ssid < 0 or ssid > 16:
        raise ValueError("Bad callsign format")

    ret = AX25Address()
    ret.callsign = cs
    ret.ssid = ssid
    
    return ret
 

def from_bytes(array, extended=False):
    '''
    Builds an AX25Packet from a bytearray.

    modulo 128 extended packets are not yet implemented.
    '''
    if not isinstance(array, bytearray):
        raise TypeError("Function takes bytearray")

    if len(array) < 15:
        raise ValueError("Packet is too short to process")

    packet = AX25Packet()

    # Pull out the destination and source from the packet
    (last, packet.dest) = bytes_to_address(array[0:7])
    if(last):
        raise ValueError("Unexpected stop of address section")
    (last, packet.src) = bytes_to_address(array[7:14])

    # Pull out each repeater
    offset = 2 * 7
    while not last:
        addr = array[offset:offset+7]

        # TODO: AX.25 spec only allows for 2 repeaters, not 8. But,
        #       APRS allows for up to 8 repeaters. Resolve?
        if len(addr) != 7 or len(packet.digipeaters) >= 8:
            raise ValueError("Address section not terminated")

        (last, addr) = bytes_to_address(addr)
        packet.digipeaters.append(addr)
        offset += 7

    if offset >= len(array):
        raise ValueError("Not enough bytes left for control")

    if not extended:
        packet.control = array[offset]
        offset += 1

        # We'll pull these fields here, but not all frames contain
        # this information. 
        packet.recv_seq = packet.control >> 5
        packet.pf_bit = (packet.control & 0x10) == 0x10
        packet.send_seq = (packet.control & 0x0c) >> 2

        # Determine the frame type, and fill / clear additonal fields
        if (packet.control & 0x01) == 0x00:
            packet.frame_type = 'I'
        elif (packet.control & 0x03) == 0x01:
            packet.frame_type = 'S'
            packet.supervisory_bits = packet.send_seq
            packet.send_seq = None
        elif (packet.control & 0x03) == 0x03:
            packet.recv_seq = None
            packet.send_seq = None
            packet.unnumbered_fm_bits = (packet.control & 0xec)

            if packet.unnumbered_fm_bits == 0:
                packet.frame_type = 'UI'
            else:
                packet.frame_type = 'U'
        else:
            raise ValueError("Invlid frame type!")

    else:
        raise NotImplementedError("Extended control field not implemented yet!")

    # I and UI frames contain the protocol ID byte 
    # (ie: first byte of info segment)
    if packet.frame_type in ['I', 'UI']:
        if offset >= len(array):
            raise ValueError("Not enough bytes left for protocol_id")

        packet.protocol_id = array[offset]
        offset += 1

    # The rest of the buffer is info now.
    packet.info = array[offset:]

    return packet
    
def dump(packet):
    '''
    Returns a string representing the packet in TNC-2 format

    Format:
        SRC>DEST,RPT1,RPT2:INFO
    '''

    ret = '%s>%s' % (packet.src, packet.dest)

    for station in packet.digipeaters:
        ret += ',%s' % station

    ret += ':%s' % packet.info

    return ret
