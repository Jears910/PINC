#Use --len(str.encode('utf-8'))-- to get str length in bytes
if((int((len(str(hex(Frame[0]))) -2) / 2)) == 7):
	if(Frame[0] == 0xaaaaaaaaaaaaaa):
		print("Valid Preamble")
	else:
		print("Invalid preamble")
else:
	print("Invalid Preamble length")
