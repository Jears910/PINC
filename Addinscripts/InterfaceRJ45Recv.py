#Use --len(str.encode('utf-8'))-- to get str length in bytes
if((int((len(str(hex(Frame[0]))) -2) / 2)) == 7):
	if(Frame[0] == 0xaaaaaaaaaaaaaa):
		print("Valid Preamble")
		if(Frame[1] == 0xab):
			print("Valid sfd")
			if(Frame[2] == globals()[Interface2].MAC or Frame[2] == 0xffffffffffff):
				print("This frame is mine")
		else:
			print("Invalid sfd")
	else:
		print("Invalid preamble")

