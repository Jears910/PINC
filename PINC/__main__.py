#! /usr/bin/env python3
# Distributed under the terms of the GPL v3
import os
import copy
import time
import sys
import threading
import DefaultClasses
import gi
from gi.repository import GLib

#Set paths to the right path
config_dir = GLib.get_user_config_dir()
PINC_dir = os.path.join(GLib.get_user_data_dir(),"PINC")

#-------------Import Addins--------------------
#Needs Improving!
sys.path.append(PINC_dir)
import Addins
from Addins import *
for Adds in Addins.allfiles:
	globals()[Adds[6:]] = globals()[Adds].main()
	globals()[Adds[6:]].AddMod = str(Adds)

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
		if(isinstance(globals()[DevType], DefaultClasses.NetDevice) and not DevType in ActiveDevices and not DevName in ActiveDevices):
			print("Creating Device " + DevName + " from " + DevType)
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
	if(ParentDev in ActiveDevices):
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
	if(globals()[ConnectorType].Connector1 == globals()[Interface1].Connector and \
	globals()[ConnectorType].Connector2 == globals()[Interface2].Connector and \
	Interface1 in ActiveInterfaces and Interface2 in ActiveInterfaces and ConnectorName not in ActiveConnectors):
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
			RecvInterface = globals()[Interface2]
			try:
				pass
				Packet, Protocol, ChildInterface = globals()[RecvInterface.AddMod].recv(Frame, globals()[Interface1], globals()[Interface2])
			except:
				print("")
			#Tell the device what and from where it recieved
			RecvDevice = globals()[RecvInterface.ParentDev]
			globals()[RecvDevice.AddMod].recv(Packet, Protocol, ChildInterface)
			#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!implement recv function in the net device
		else:
			print("Make sure you selected two existing Interfaces that are connected")
	else:
		print("The string needs to be a list but was given a " + str(type(Frame)))

def Rename( OldName, NewName ):
#Check if the Pbject exists and if it is a Device, Interface or Connector
	if(OldName in ActiveDevices):
		#Check if the new name is still available
		if(NewName not in ActiveDevices and not NewName in ActiveInterfaces and not NewName in ActiveConnectors):
			#Give the child Interfaces the new name
			InterfaceNumber = 0
			for Interface in globals()[OldName].Interfaces:
				if(not Interface == None):
					globals()[Interface].ParentDev = NewName
			#Make the new device
			globals()[NewName] = globals()[OldName]
			#manipulate the Active Devices list
			ElementPlace = 0
			for Element in ActiveDevices:
				if(Element == OldName):
					ActiveDevices[ElementPlace] = NewName
				ElementPlace += 1
			#delete the old device
			del globals()[OldName]
			print("Renamed Device " + OldName + " to " + NewName)
			return globals()[NewName]
		else:
			print("This name has already been given to something else")
	elif(OldName in ActiveInterfaces):
		#check if the name is still available
		if(NewName not in ActiveDevices and not NewName in ActiveInterfaces and not NewName in ActiveConnectors):
			#Go through The parent devices Interfaces and rename it
			InterfaceNumber = 0
			for Interface in globals()[globals()[OldName].ParentDev].Interfaces:
				if(globals()[globals()[OldName].ParentDev].Interfaces[InterfaceNumber] == OldName):
					globals()[globals()[OldName].ParentDev].Interfaces[InterfaceNumber] = NewName
				InterfaceNumber += 1
			#Check the Connected Connector and give it the new name
			if(globals()[globals()[OldName].ConnectedConnector].Interface1 == OldName):
				globals()[globals()[OldName].ConnectedConnector].Interface1 = NewName
			if(globals()[globals()[OldName].ConnectedConnector].Interface2 == OldName):
				globals()[globals()[OldName].ConnectedConnector].Interface2 = NewName
			#Create the new interface
			globals()[NewName] = globals()[OldName]
			#Replace the Interface Name in the actie Interfaces list
			ElementPlace = 0
			for Element in ActiveInterfaces:
				if(Element == OldName):
					ActiveInterfaces[ElementPlace] = NewName
				ElementPlace += 1
			#Remove the old Interface
			del globals()[OldName]
			print("Renamed Interface " + OldName + " to " + NewName)
			return globals()[NewName]
		else:
			print("This name has already been given to something else")
	elif(OldName in ActiveConnectors):
		#check if the name is still available
		if(NewName not in ActiveDevices and not NewName in ActiveInterfaces and not NewName in ActiveConnectors):
			#Give the connected Interfaces the new name
			globals()[globals()[OldName].Interface1].ConnectedConnector = NewName
			globals()[globals()[OldName].Interface2].ConnectedConnector = NewName
			#Create the new connector
			globals()[NewName] = globals()[OldName]
			#Replave the connector name in the active connector list
			ElementPlace = 0
			for Element in ActiveConnectors:
				if(Element == OldName):
					ActiveConnectors[ElementPlace] = NewName
				ElementPlace += 1
			del ElementPlace
			#delete the old Connector
			del globals()[OldName]
			print("Renamed Connector " + OldName + " to " + NewName)
			return globals()[NewName]
		else:
			print("This name has already been given to something else")
	else:
		print("Object to be renamed not found")

#This function sucks, realy, it's horrible
def Delete( DeleteName ):
	if(DeleteName in ActiveDevices):
		for Interface in globals()[DeleteName].Interfaces:
			if(Interface != None):
				Delete(Interface)
		del globals()[DeleteName]
		DeviceNumber = 0
		for Device in ActiveDevices:
			if(Device == DeleteName):
				ActiveDevices[DeviceNumber] = None
			DeviceNumber += 1
		print("Deleted Device " + DeleteName)
	elif(DeleteName in ActiveInterfaces):
		print("Deleted Interface " + DeleteName)
		DeleteInterface = DeleteName
		DeleteConnector = globals()[DeleteInterface].ConnectedConnector
		InterfaceNumber = 0
		for Interface in ActiveInterfaces:
			if(Interface == DeleteInterface):
				ActiveInterfaces[InterfaceNumber] = None
			InterfaceNumber += 1
		for Interface in globals()[globals()[DeleteInterface].ParentDev].Interfaces:
			if(Interface == DeleteInterface):
				DeleteInterface = None
		del globals()[DeleteName]
		Delete(DeleteConnector)
	elif(DeleteName in ActiveConnectors):
		InterfaceSlot = 0
		if(globals()[DeleteName].Interface1 in globals()):
			globals()[globals()[DeleteName].Interface1].ConnectedConnector = None
		if(globals()[DeleteName].Interface2 in globals()):
			globals()[globals()[DeleteName].Interface2].ConnectedConnector = None
		ConnectorNumber = 0
		for Connector in ActiveConnectors:
			if(Connector == DeleteName):
				ActiveConnectors[ConnectorNumber] = None
			ConnectorNumber += 1
		del globals()[DeleteName]
		print("Deleted Connector " + DeleteName)
	else:
		print("Couldn't find " + DeleteName + " to delete")

#The frame sending needs to happen in the background so that it doesn't lock up the whole program during its delay, this function allows to run things in bg
#This Needs improvement on the way it passes its arguments !
def run_bg( bg_process ):
	if(isinstance(bg_process, str)):
		#I'm resolving the given Process here so that it is readable for threads
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
		bg_process_process = bg_process[None:firstBracket]
		bg_process_args = bg_process[firstBracket+1:lastBracket]
		process_bg_thread = threading.Thread(target=eval(bg_process_process), args=(eval(bg_process_args)))
		return process_bg_thread.start()
	else:
		print("bg_run needs a string but was given " + str(type(bg_process)))

# Test function calls, these are gonna be removed when there is an interactive conslole
CreateDevice("PC1", "PINCPC")
AddInterface("RJ45PC1", "RJ45Ethernet", "PC1", 0)
CreateDevice("PC2", "PINCPC")
AddInterface("RJ45PC2", "RJ45Ethernet", "PC2", 0)
ConnectInterfaces("RJ45PC1PC2", "RJ45", "RJ45PC1", "RJ45PC2")
Rename("RJ45PC1PC2", "test")
Rename("RJ45PC1", "RJ45TestName")
Rename("PC1", "PCTest")
run_bg('SendFrame([0xAAAAAAAAAAAAAA, 0xAB, 0xffffffffffff, RJ45TestName.MAC, 0x0800, [0x0142145761757171717572457846384284248234245644248224242454241244243, "abbcdf"], 2078830327, 0x000000000000000000000000], "RJ45TestName", "RJ45PC2")')

#--------------Gtk Mode----------------------------------
if("--gtk" in sys.argv or "-g" in sys.argv):
	pass
	gi.require_version('Gtk', '3.0')
	from gi.repository import Gtk
	from gi.repository import Gdk
	class PINCWindowMain(Gtk.Window):
		def __init__(self):
			Gtk.Window.__init__(self, title="PINC")
			#self.MenuBar = Gtk.MenuBar()
			#self.add(self.MenuBar)
			self.DrawingArea = Gtk.DrawingArea()
			self.add(self.DrawingArea)
			self.DrawingArea.connect("draw", self.Draw, self.DrawingArea)
		def Draw(self, widget, event , Area):
			cr = widget.get_property('window').cairo_create()
			#Get the foreground color (What the fuck Gtk, why is this so much for a color)
			foregroundColor = Gtk.StyleContext.get_color(WindowMain.DrawingArea.get_style_context(), WindowMain.DrawingArea.get_state())
			#Set the default line color
			cr.set_source_rgb(foregroundColor.red, foregroundColor.green, foregroundColor.blue)
#--------- From here on it is just tests that will be removed
			cr.move_to(20, 20)
			cr.line_to(30, 30)
			cr.stroke()
			cr.move_to(40, 40)
			cr.line_to(55, 35)
			cr.stroke()

	WindowMain = PINCWindowMain()
	WindowMain.connect("destroy", Gtk.main_quit)
	WindowMain.show_all()
	Gtk.main()

#-------------------CLI Mode------------------------------
#elif "--cli" in sys.argv or "-c" in sys.argv:
else: #I want to be able to use it without typing -c all the time
	print("\033[96;1mCLI Mode")
	stopcli = False
	while stopcli == False:
		cliinput = input("\033[92;1mPINC > \033[0m").split(" ")
		#This Crates a new Device by using the correct function
		if(cliinput[0] == "CreateDevice"):
			if(len(cliinput) != 3 or "--help" in cliinput or "-h" in cliinput):
				print("This creates a new Device\nUsage:\nCreateDevice \033[1m[DeviceName] [DeviceType]\033[0m")
			else:
				CreateDevice(cliinput[1], cliinput[2])
		#This adds a Interface to a Device
		elif(cliinput[0] == "AddInterface"):
			if(len(cliinput) != 5 or "--help" in cliinput or "-h" in cliinput):
				print("This creates a new Interface in an existing Device\nUsage:\nAddInterface \033[1m[Interface Name] [Interface Type] [Parent Device] [Device Slot]\033[0m")
			else:
				AddInterface(cliinput[1], cliinput[2], cliinput[3], cliinput[4])
		#This connects two interfaces
		elif(cliinput[0] == "ConnectInterfaces"):
			if(len(cliinput) != 5 or "--help" in cliinput or "-h" in cliinput):
				print("This creates a new Connection between two existing Interfaces\nUsage:\nConnectInterfaces \033[1m[Connector Name] [Connector Type] [Interface 1] [Interface 2]\033[0m")
			else:
				ConnectInterfaces(cliinput[1], cliinput[2], cliinput[3], cliinput[4])
		#This renames an object
		elif(cliinput[0] == "Rename"):
			if(len(cliinput) != 3 or "--help" in cliinput or "-h" in cliinput):
				print("This Renames existing Devices, Interfaces and Connectors\nUsage:\nRename \33[1m[Old Name] [NewName]\033[0m")
			else:
				Rename(cliinput[1], cliinput[2])
		elif(cliinput[0] == "Delete"):
			if(len(cliinput) != 2 or "--help" in cliinput or "-h" in cliinput):
				print("This Deletes an existing Device, Interface or Connector\nUsage:\nDelete \33[1m[Object Name]\033[0m")
			else:
				Delete(cliinput[1])
		#List active objects
		elif(cliinput[0] == "ListDevices"):
			print(ActiveDevices)
		elif(cliinput[0] == "ListInterfaces"):
			print(ActiveInterfaces)
		elif(cliinput[0] == "ListConnectors"):
			print(ActiveConnectors)
		#allows you to exit the commandline
		elif(cliinput[0] == "exit"):
			stopcli = True
		#help command !!!!!!!!!!!!!!!!! Update if you change anything
		elif(cliinput[0] == "help"):
			print("CreateDevice \033[1m[DeviceName] [DeviceType]\033[0m\nThis creates a new Device\n")
			print("AddInterface \033[1m[Interface Name] [Interface Type] [Parent Device] [Device Slot]\033[0m\nThis creates a new Interface in an existing Device\n")
			print("ConnectInterfaces \033[1m[Connector Name] [Connector Type] [Interface 1] [Interface 2]\033[0m\nThis creates a new Connection between two existing Interfaces\n")
			print("Rename \033[1m[Old Name] [New Name]\033[0m\nThis renames existing Devices, Interfaces and Connectors\n")
			print("Usage:\nDelete \33[1m[Object Name]\033[0m\nThis Deletes an existing Device, Interface or Connector\n")
			print("ListDevices\nThis lists all active Devices\n")
			print("ListInterfaces\nThis lists all active Interfaces\n")
			print("ListConnectors\nThis lists all active Connectors\n")
		else:
			print("Couldn't recognize \"" + cliinput[0] + "\" as a PINC-CLI command. Get help with the \033[1mhelp\033[0m command")
