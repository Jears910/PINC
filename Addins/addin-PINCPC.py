def main():
	import DefaultClasses
	class PINCPC(DefaultClasses.NetDevice):
		Interfaces = [None, None]
		def __init__(self, label):
			self.label = label
		def recv(self, Packet, Protocol):
			print(str(self) + " received the packet " + str(Packet) + " of the type " + Protocol)
			if(Protocol == "IPv4"):
				if(type(Packet) == list and len(Packet) == 15 or len(Packet) == 14):
				# Version check
					if(Packet[0] == 4):
						print("Is v4")
						# IHL (Unrealistic, might make an option later)
						if(Packet[1] <= 16 and Packet[1] >= 5):
							print("Valid IHL")
							#Type of Service 
							#if(Packet[2] )
						else:
							print("Invalid IHL")
					else:
						print("not v4")
				else:
					print("Not a valid IP Packet")
	return PINCPC
