# gr-APRS
GNU Radio Hierarchial Block(s) to Test and Receive APRS Packet (with examples). Tested on GNU Radio v3.7.10.

## Installations
This OOT Module is built upon GNU Radio hierarchial block scheme. The hierarchial block itself is "transparently" built graphically / visually using GRC. The hier blocks are provided in the gr-APRS/HierBlock folder.
Installation steps :
* `git clone https://github.com/handiko/gr-APRS.git`
* `cd gr-APRS/HierBlock/`
* `gnuradio-companion AFSK_Demod.grc` **AFSK_Demod.grc** should be installed **first**.
* **Click RUN** button on GNU Radio companion (It will do nothing on foreground, since it will just build and install the Hier Block). And then **Close**.
* **Open the GNU Radio**. The new Hier Block will be listed under APRS module.

And then **very important** steps :
* `cd`
* `sudo cp gr-APRS/Module/packet.py /usr/lib/python2.7/` This will copy **packet.py** files from **gr-APRS/Module/** into **/usr/lib/python2.7/** directory. Without this, the **HDLC to AX.25** block will not run.

Finish, and now you can open grc files on **gr-APRS/Examples/** or **gr-APRS/TestScripts/** and run it.
