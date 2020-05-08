def main():
	import DefaultClasses
	#Name														ConType	ParentDev	ConnectedConnector	Attributes
	#random.randint(0x000000000001, 0xfffffffffffe) This is gonna be the mac adress later
#	RJ45Ethernet = DefaultClasses.NetInterface(	"RJ45",	None,			None,						0xabcdef012345)
	class RJ45Ethernet(DefaultClasses.NetInterface):
		Connector = "RJ45"
		MAC = 0xabcdef012345
		def __init__(self, ParentDev):
			self.ParentDev = ParentDev

		def recv(self, Frame):
			import ethertype
			import crc32
		#Use --len(str.encode('utf-8'))-- to get str length in bytes
			def ResolveEthertype(TypeField):
				try:
					PayloadProtocol = ethertype.ethertype[TypeField]
					return PayloadProtocol
				except:
					print(str(TypeField) + " This is an invalid ethertype and I'm discarding this package")
					print("Available ethertypes: " + ethertype.ethertype)
					return 1

			if((int((len(str(hex(Frame[0]))) -2) / 2)) == 7):
				print(Frame[2:6])
				#Check Preamble
				if(Frame[0] == 0xaaaaaaaaaaaaaa):
					#check sfd
					if(Frame[1] == 0xab):
						#check if the frame is mine or not
						if(Frame[2] == self.MAC or Frame[2] == 0xffffffffffff):
							#check if the sender has a valid mac address
							if(Frame[3] >=0x000000000000 and Frame[3] <= 0xffffffffffff):
								TypeName = ResolveEthertype(Frame[4])
								if(not TypeName == 1):
									if(crc32.crc32(Frame[2:6]) == Frame[6]):
										return Frame[5], TypeName
									else:
										print("The CRC checksums don't match, please resend")
										return 1
							else:
								print("This sender doesn't even have a valid MAC-Adress, I'm discarding it")
								return 1
						else:
							print("This isn't my frame, I'm discarding it")
							return 1
					else:
						print("Invalid sfd")
						return 1
				else:
					print("Invalid preamble")
					return 1
		def send(self, Packet, Receiver, TypeName, SendQueue):
			import ethertype
			import crc32
			#Add ethertype
			Frame = []
			#try:
			Preamble = 0xAAAAAAAAAAAAAA
			Frame.append(Preamble)
			SFD = 0xAB
			Frame.append(SFD)
			RecvMAC = Receiver
			Frame.append(RecvMAC)
			SendMAC = self.MAC
			Frame.append(SendMAC)
			FrameEthertype = ethertype.ethertypeRev[TypeName]
			Frame.append(FrameEthertype)
			Frame.append(Packet)
			Checksum = crc32.crc32(Frame[2:6])
			Frame.append(Checksum)
			print(Frame)
			SendQueue.append(Frame)
			return (Frame, self)
			#except:
			#	return 'print("Send Error")'
	return RJ45Ethernet

