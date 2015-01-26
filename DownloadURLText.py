import urllib2

dataURL = "https://code.wireshark.org/review/gitweb?p=wireshark.git;a=blob_plain;f=manuf;hb=HEAD"

fd = open("downloaded.txt","w")

for line in urllib2.urlopen(dataURL):
	fd.write(line)
	
fd.close()
