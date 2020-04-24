def main():
	import DefaultClasses
	#Name								UI			Interface Slots									Recv Script				Send Script
	PINCSwitch =	DefaultClasses.NetDevice(	None,	[None, None, None, None, None, None, None],	"PINCSitchRecv.py",	"PINCSwitchSend.py")
	return PINCSwitch
