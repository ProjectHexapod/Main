Required for 2.4 kernels that require FT2232 support only.  
FT2232 support included in kernel 2.6.9 or greater.  
Developed by Bill Ryder.  Instructions in ReadMe file.  
All other devices included in kernel 2.4.20 or greater (see ReadMe for 232R device support).



Instructions to install new driver

You may require the sources matching the current kernel to be installed on your system (and built). 
There are many helpfull websites that can assist you with this step and it isnt as daunting as you first think!
Try http://www.osnews.com/story.php?news_id=2949&page=2 as a first step if the link is still available.


To install the ftdi_sio driver use the following steps:

1. Create a temporary folder in your linux machine.
2. Extract the files from ftdi_sio.tar.gz file to your temporary folder
	"gunzip ftdi_sio.tar.gz"
	"tar -xvf ftdi_sio.tar"
3. Build the driver
	"make"
4. Plug in your ftdi device
5. Check to see if default driver was loaded
	"lsmod" - you will see ftdi_sio if a driver is loaded
6. Remove the default installed driver
	"rmmod ftdi_sio"
7. Install the newly built driver
	"insmod ftdi_sio.o"


NOTES: 
	1.This driver was adapted from the 2.4.32 kernel to support both the 2232C and 232R chip
	2.There is no need to follow this procedure if you want 232R chip supprt. The 232BM driver will 
	be sufficient.Changes made to the driver for the 232R chip are purly cosmetic (plug/unplug will appear as a 232R chip in 
	the kernel log).