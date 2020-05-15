def main():
	import DefaultClasses
	#Name											ConType1		ConType2		Interface1	Interface2	Latency
#	RJ45 = DefaultClasses.NetConnector(	"RJ45",		"RJ45",		None,			None,			5)
	class RJ45(DefaultClasses.NetConnector):
		Connector1 = "RJ45"
		Connector2 = "RJ45"
		Latency = 5
		def __init__(self, label, Interface1, Interface2):
			self.label = label
			self.Interface1 = Interface1
			self.Interface2 = Interface2
	return RJ45
