#! /usr/bin/python
import os
import copy
import time
import sys
import threading

#--------------Default Classes------------------
class NetDevice (object):
	'Network Device'
	# If the device should have a UI (in form of a CLI), the py File goes here, otherwise put None here
	UI = ""
	# Always define Interface slots as None, they are added later
	Interfaces = []
	PackageRecv = ""
	PackageSend = ""
	def __init__(self, UI, Interfaces, PackageRecv, PackageSend):
		self.UI = UI
		self.Interfaces = Interfaces
		self.PackageRecv = PackageRecv
		self.PackageSend = PackageSend

class NetInterface (object):
	'Interfaces that get plugged into a NetDevice'
	Connector = ""
	# The interface performs Package Handling when it Recieves or Sends a Package. These Routins are defined in a Python File
	FrameHandleRecv = ""
	FrameHandleSend = ""
	ParentDev = ""
	ConnectedConnector = ""
	Attributes = []
	def __init__(self, Connector, FrameHandleRecv, FrameHandleSend, ParentDev, ConnectedConnector, Attributes):
		self.Connector = Connector
		self.FrameHandleRecv = FrameHandleRecv
		self.FrameHandleSend = FrameHandleSend
		self.ParentDev = ParentDev
		self.ConnectedConnector = ConnectedConnector
		self.Attributes = Attributes

class NetConnector (object):
	'Cables, Adapters, ...'
	Connector1 = ""
	Connector2 = ""
	Interface1 = ""
	Interface2 = ""
	#Latency is provided in ms
	Latency = 0
	def __init__(self, Connector1, Connector2, Interface1, Interface2, Latency):
		self.Connector1 = Connector1
		self.Connector2 = Connector2
		self.Interface1 = Interface1
		self.Interface2 = Interface2
		self.Latency = Latency

#-------------Import Addins--------------------
#Needs Improving!

for filename in os.listdir(os.path.join(os.getcwd(), "Addins")):
	addfile = os.path.join(os.getcwd(), "Addins", filename)
	exec(open(addfile).read())
del filename
del addfile

#----------Lists Needed by functions----------
#This is the list with all the existing devices
ActiveDevices = []
#This is the list with all the active interfaces
ActiveInterfaces = []
#This is the list with all the active connectors
ActiveConnectors = []

#------------Functions-------------------------
# This is the function to create a new device
def CreateDevice( DevName, DevType ):
	try:
		if isinstance(globals()[DevType], NetDevice) and not DevType in ActiveDevices and not DevName in ActiveDevices:
			print("Creating Device")
			# To create a device the object is cloned and its name added to a list
			"".join([vars()["DevType"], ".Interfaces"])
			globals()[DevName] = copy.deepcopy(globals()[DevType])
			ActiveDevices.append(DevName)
			return globals()[DevName]
		else:
			print("Make sure your Devicetype is a valid Devicetype")
	except:
		print("Make sure your Devicetype is a valid Devicetype")

# This funcion adds a Network card to an Active device
def AddInterface( InterfaceName, InterfaceType, ParentDev, DevSlot ):
	if ParentDev in ActiveDevices:
		print("Creating Interface " + InterfaceName + " from " + InterfaceType + " in " + ParentDev)
		globals()[InterfaceName] = copy.deepcopy(globals()[InterfaceType])
		globals()[InterfaceName].ParentDev = ParentDev
		globals()[ParentDev].Interfaces[int(DevSlot)] = InterfaceName
		ActiveInterfaces.append(InterfaceName)
		return globals()[InterfaceName]
	else:
		print("Make sure you choose a valid device")

# This function connects two Interfaces with a connector
def ConnectInterfaces( ConnectorName, ConnectorType, Interface1, Interface2 ):
	#The Interfaces must be active and the Connector Types must match
	if globals()[ConnectorType].Connector1 == globals()[Interface1].Connector and \
	globals()[ConnectorType].Connector2 == globals()[Interface2].Connector and \
	Interface1 in ActiveInterfaces and Interface2 in ActiveInterfaces and ConnectorName not in ActiveConnectors:
		print("Creating Connection " + ConnectorName + " from the type " + ConnectorType + " between " + Interface1 + " and " + Interface2)
		globals()[ConnectorName] = copy.deepcopy(globals()[ConnectorType])
		globals()[ConnectorName].Interface1 = Interface1
		globals()[ConnectorName].Interface2 = Interface2
		globals()[Interface1].ConnectedConnector = ConnectorName
		globals()[Interface2].ConnectedConnector = ConnectorName
		ActiveConnectors.append(ConnectorName)
		return globals()[ConnectorName]
	else:
		print("Could not create Connector, check that the Connector Types match, that you choose valid interfaces and a unique name")
#This function is used to send a frame between Interfaces
#The Frame is the whole actual frame as a table, each field in the frame can be split that way.
def SendFrame( Frame, Interface1, Interface2 ):
	if(isinstance( Frame, list )):
	#The interfaces must be connected
		if globals()[Interface1].ConnectedConnector == globals()[Interface2].ConnectedConnector:
			time.sleep((globals()[globals()[Interface1].ConnectedConnector].Latency)/1000)
			#Tell the Interface it recieved a frame
			exec(open(os.path.join(os.getcwd(), "Addinscripts", globals()[Interface2].FrameHandleRecv)).read())
		else:
			print("Make sure you selected two existing Interfaces that are connected")
	else:
		print("The string needs to be a list but was given a " + str(type(Frame)))

#The frame sending needs to happen in the background so that it doesn't lock up the whole program, this function allows to run things in bg
#This Needs improvement on the way it passes its arguments !!!!!!!!!!!!!!!!!!!!!!!!!!!!
def run_bg( bg_process ):
	if(isinstance(bg_process, str)):
		location = 0
		firstBracket = None
		lastBracket = None
		for character in bg_process:
			location += 1
			if(character == "("):
				firstBracket = location - 1
				break
		location = 0
		for character in bg_process:
			location += 1
			if(character == ")"):
				lastBracket = location - 1
		bg_process = [bg_process]
		bg_process_process = bg_process[None:firstBracket]
		bg_process_args = bg_process[firstBracket+1:lastBracket]
		print(bg_process_process)
		print(bg_process_args)
#CONTINUE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 
		process_bg_thread = threading.Thread(target=bg_process_process, args=bg_process_args)
		process_bg_thread.start()
	else:
		print("bg_run needs a string but was given " + str(type(bg_process)))

# Test function calls, these are gonna be removed when there is an interactive conslole
CreateDevice("Switch1", "PINCSwitch")
AddInterface("RJ45Sw1", "InterfaceRJ45", "Switch1", 0)
CreateDevice("Switch2", "PINCSwitch")
AddInterface("RJ45Sw2", "InterfaceRJ45", "Switch2", 0)
ConnectInterfaces("RJ45Sw1Sw2", "RJ45", "RJ45Sw1", "RJ45Sw2")
run_bg('SendFrame([123, 34234, 32423], "RJ45Sw1", "RJ45Sw2")')

#-------------------CLI Mode------------------------------
if "--gtk" in sys.argv or "-g" in sys.argv:
	pass
	#import gi
	#gi.require_version("Gtk", "3.0")
	#from gi.repository import Gtk
	#class PINCWindowMain(Gtk.Window):
	#	def __init__(self):
	#		Gtk.Window.__init__(self, title="PINC")
	#		
	#		#self.MenuBar = Gtk.MenuBar()
	#		#self.add(self.MenuBar)
	#		self.Toolbar = Gtk.Toolbar()
	#		self.add(self.Toolbar)
	#WindowMain = PINCWindowMain()
	#WindowMain.connect("destroy", Gtk.main_quit)
	#WindowMain.show_all()
	#Gtk.main()

#elif "--cli" in sys.argv or "-c" in sys.argv:
else: #I want to be able to use it without typing -g all the time
	print("\033[96;1mCLI Mode")
	stopcli = False
	while stopcli == False:
		cliinput = input("\033[92;1mPINC > \033[0m").split(" ")
		#This Crates a new Device by using the correct function
		if cliinput[0] == "CreateDevice":
			if len(cliinput) != 3 or "--help" in cliinput or "-h" in cliinput:
				print("This Creates a new Device\nUsage:\nCreateDevice \033[1m[DeviceName] [DeviceType]\033[0m")
			else:
				CreateDevice(cliinput[1], cliinput[2])
		#This adds a Interface to a Device
		elif cliinput[0] == "AddInterface":
			if len(cliinput) != 5 or "--help" in cliinput or "-h" in cliinput:
				print("This Creates a new Interface in an existing Device\nUsage:\nAddInterface \033[1m[Interface Name] [Interface Type] [Parent Device] [Device Slot]\033[0m")
			else:
				AddInterface(cliinput[1], cliinput[2], cliinput[3], cliinput[4])
		#This connects two interfaces
		elif cliinput[0] == "ConnectInterfaces":
			if len(cliinput) != 5 or "--help" in cliinput or "-h" in cliinput:
				print("This Creates a new Connection between two existing Interfaces\nUsage:\nConnectInterfaces \033[1m[Connector Name] [Connector Type] [Interface 1] [Interface 2]\033[0m")
			else:
				ConnectInterfaces(cliinput [1], cliinput[2], cliinput[3], cliinput[4])
		#List active objects
		elif cliinput[0] == "ListDevices":
			print(ActiveDevices)
		elif cliinput[0] == "ListInterfaces":
			print(ActiveInterfaces)
		elif cliinput[0] == "ListConnectors":
			print(ActiveConnectors)
		#allows you to exit the commandline
		elif cliinput[0] == "exit":
			stopcli = True
		#help command !!!!!!!!!!!!!!!!! Update if you change anything
		elif cliinput[0] == "help":
			print("CreateDevice \033[1m[DeviceName] [DeviceType]\033[0m\nThis Creates a new Device\n")
			print("AddInterface \033[1m[Interface Name] [Interface Type] [Parent Device] [Device Slot]\033[0m\nThis Creates a new Interface in an existing Device\n")
			print("ConnectInterfaces \033[1m[Connector Name] [Connector Type] [Interface 1] [Interface 2]\033[0m\nThis Creates a new Connection between two existing Interfaces\n")
			print("ListDevices\nThis lists all active Devices\n")
			print("ListInterfaces\nThis lists all active Interfaces\n")
			print("ListConnectors\nThis lists all active Connectors\n")
		else:
			print("Couldn't recognize \"" + cliinput[0] + "\" as a PINC-CLI command. Get help with the \033[1mhelp\033[0m command")
