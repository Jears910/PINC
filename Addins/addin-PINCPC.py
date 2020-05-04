def main():
	import DefaultClasses
	#Name											UI		Interface Slots
	class PINCPC(DefaultClasses.NetDevice):
		Interfaces = [None, None]
		def __init__(self):
			pass
		def recv(self, Packet, Protocol):
			print(str(self) + " received the packet " + str(Packet))
	return PINCPC
