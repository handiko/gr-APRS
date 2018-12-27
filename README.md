# gr-APRS
GNU Radio Hierarchial Block(s) to Test and Receive APRS Packet (with examples). Tested on GNU Radio v3.7.10 / Linux Ubuntu.

![alt text](https://github.com/handiko/gr-APRS/blob/master/Pic/gnuradio_logo.svg)

## Dependency
* **GNU Radio**. Please check out https://www.gnuradio.org/ or https://github.com/gnuradio/gnuradio

## Installations
This OOT Module is built upon GNU Radio hierarchial block scheme. The hierarchial block itself is "transparently" built graphically / visually using GRC. The hier blocks are provided in the gr-APRS/HierBlock folder.
Installation steps :
* `git clone https://github.com/handiko/gr-APRS.git`
* `cd gr-APRS/HierBlock/`
* `gnuradio-companion AFSK_Demod.grc` **AFSK_Demod.grc** should be installed **first**.
* **Click RUN** (F6) button on GNU Radio companion (It will do nothing on the foreground, since it will just build and install the Hier Block silently). And then **Close**.
* `gnuradio-companion APRS_Rx.grc` **APRS_Rx.grc** should be installed **after** AFSK_Demod.grc.
* Again, **Click RUN** (F6) button. And then Close.
* **Open the GNU Radio**. The new Hier Block will be listed under APRS module.
![alt text](https://github.com/handiko/gr-APRS/blob/master/Pic/successful_installation.png)

And then **very important** steps :
* `cd`
* `sudo cp gr-APRS/Module/packet.py /usr/lib/python2.7/` This will copy **packet.py** files from **gr-APRS/Module/** into **/usr/lib/python2.7/** directory. Without this, the **HDLC to AX.25** block will not run.

Finish, and now you can open grc files on **gr-APRS/Examples/** or **gr-APRS/TestScripts/** and run it.

### About The HDLC to AX.25 block
This block which functions to convert HDLC data into TNC2 APRS formats is constructed from the "Python Block" which native to the GNU Radio Companion. To build one yourself:
* From GNU Radio Core module, under Misc, add Python Block into your flowgraph.
* Double Click that block to open the properties and then click Open in Editor. If then you asked about which editor to choose, just select default or any editor you prefer.
* In the editor, copy and paste python code from **gr-APRS/Module/epb.py**, safe, close, and hit OK.
* Now your Python Block should be turned into HDLC to AX.25 Block, have message i/o ports which labelled as "hdlc in" and "ax25 out".
* Done !

## Hier Blocks
All the hier blocks are constructed graphically using GNU Radio Companion. AFSK Demod hier block is required by the APRS Rx hier block (hier block which contains another hier block within), so it should be installed first.

### AFSK Demod
![alt text](https://github.com/handiko/gr-APRS/blob/master/Pic/AFSK_Demod.grc.png)

### APRS Rx
![alt text](https://github.com/handiko/gr-APRS/blob/master/Pic/APRS_Rx.grc.png)

## Examples
There is some grc examples included in **gr-APRS/Examples** and **gr-APRS/TestScripts** folder. WAV files are also included in the **gr-APRS/WAV** for testing purposes.

### APRS RX RTL
From **gr-APRS/Examples/APRS_RX_RTL.grc**. This examples utilizes the low cost RTL SDR dongle for receiving APRS signal on 144.390 Mhz (for usage on another frequency, please change the frequency in the grc).
![alt text](https://github.com/handiko/gr-APRS/blob/master/Pic/APRS_RX_RTL.grc.png)

### APRS SCARD
From **gr-APRS/Examples/APRS_SCARD.grc**. This examples utilizes the onboard sound card for the usage with a VHF Radio receiver. Audio from the Radio SPK output should be fed into the MIC input of your soundcard.
![alt text](https://github.com/handiko/gr-APRS/blob/master/Pic/APRS_SCARD.grc.png)

### APRS AFSK Complete WAV
From **gr-APRS/TestScripts/APRS_AFSK_Complete_WAV.grc**. This examples will decode AFSK audio files which included in **gr-APRS/WAV**. This example mainly for testing purposes (for example, to find the best values of Mu and Gain Mu).
![alt text](https://github.com/handiko/gr-APRS/blob/master/Pic/APRS_AFSK_Complete_WAV.grc.png)

...
