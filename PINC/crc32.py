def crc32(Input):
	import binascii
	#This function should be used to calculate crc32 checksumsdef crc32(Input):
	crcBytes = bytearray()
	for element in Input:
		if(isinstance(element,int)):
			bytenumber = format(element, '0x')
		elif(isinstance(element,str)):
			bytenumber = format(int.from_bytes(element.encode('utf-8'), "big"), '0x')
		elif(isinstance(element,list)):
			bytenumber = 0
			for subelement in element:
				if(isinstance(subelement,int)):
					bytenumber += subelement
				elif(isinstance(subelement,str)):
					bytenumber += int.from_bytes(subelement.encode('utf-8'), "big")
			bytenumber = format(bytenumber, '0x')
		if(len(bytenumber) % 2):
			bytenumber = "0" + bytenumber
		appendBytes = bytearray.fromhex(bytenumber)
		crcBytes = crcBytes + appendBytes
	crc32Result = binascii.crc32(crcBytes)
	return crc32Result
