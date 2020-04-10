#Name					UI		Interface Slots								Recv Script			Send Script
PINCSwitch =	NetDevice(	None,	[None, None, None, None, None, None, None],	"PINCSitchRecv.py",	"PINCSwitchSend.py")

#Name							ConType	RecvScript				SendScript				ParentDev	ConnectedConnector	Attributes
InterfaceRJ45 = NetInterface(	"RJ45",	"InterfaceRJ45Recv.py",	"InterfaceRJ45Send.py",	None,		None,				["ab:cd:ef:01:23:45"])

#Name					ConType1	ConType2	Interface1	Interface2	Latency
RJ45 = NetConnector(	"RJ45",		"RJ45",		None,		None,		5)
