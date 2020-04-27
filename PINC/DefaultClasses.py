class NetDevice (object):
	'Network Device'
	# If the device should have a UI (in form of a CLI), the py File goes here, otherwise put None here
	UI = ""
	# Always define Interface slots as None, they are added later
	Interfaces = []
	PackageRecv = ""
	PackageSend = ""
	AddMod = ""
	def __init__(self, UI, Interfaces):
		self.UI = UI
		self.Interfaces = Interfaces

class NetInterface (object):
	'Interfaces that get plugged into a NetDevice'
	Connector = ""
	# The interface performs Package Handling when it Recieves or Sends a Package. These Routins are defined in a Python File
	ParentDev = ""
	ConnectedConnector = ""
	Attributes = []
	AddMod = ""
	def __init__(self, Connector, ParentDev, ConnectedConnector, MAC):
		self.Connector = Connector
		self.ParentDev = ParentDev
		self.ConnectedConnector = ConnectedConnector
		self.MAC = MAC

class NetConnector (object):
	'Cables, Adapters, ...'
	Connector1 = ""
	Connector2 = ""
	Interface1 = ""
	Interface2 = ""
	#Latency is provided in ms
	Latency = 0
	AddMod = ""
	def __init__(self, Connector1, Connector2, Interface1, Interface2, Latency):
		self.Connector1 = Connector1
		self.Connector2 = Connector2
		self.Interface1 = Interface1
		self.Interface2 = Interface2
		self.Latency = Latency
