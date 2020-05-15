class NetDevice (object):
	label = ""
	'Network Device'
	# If the device should have a UI (in form of a CLI), the py File goes here, otherwise put None here
	UI = ""
	# Always define Interface slots as None, they are added later
	Interfaces = []

class NetInterface (object):
	label = ""
	'Interfaces that get plugged into a NetDevice'
	Connector = ""
	# The interface performs Package Handling when it Recieves or Sends a Package. These Routins are defined in a Python File
	ParentDev = ""
	ConnectedConnector = ""
	MAC = 0x0

class NetConnector (object):
	label = ""
	'Cables, Adapters, ...'
	Connector1 = ""
	Connector2 = ""
	Interface1 = ""
	Interface2 = ""
	#Latency is provided in ms
	Latency = 0
