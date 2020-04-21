#Name								UI			Interface Slots									Recv Script				Send Script
PINCSwitch =	NetDevice(	None,	[None, None, None, None, None, None, None],	"PINCSitchRecv.py",	"PINCSwitchSend.py")

#Name									ConType	RecvScript					SendScript				ParentDev	ConnectedConnector	Attributes
RJ45Ethernet = NetInterface(	"RJ45",	"RJ45EthernetRecv.py",	"RJ45EthernetSend.py",	None,		None,				0xabcdef012345)

#Name					ConType1			ConType2	Interface1	Interface2	Latency
RJ45 = NetConnector(	"RJ45",		"RJ45",		None,		None,			5)
