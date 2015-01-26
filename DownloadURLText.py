"""
A very simple example of downloading content of a URL
"""

import urllib2, os


def downloadFile(URL="",fileName="downloaded.txt"):

	# URL to the file to be downloaded
	_dataURL = "https://code.wireshark.org/review/gitweb?p=wireshark.git;a=blob_plain;f=manuf;hb=HEAD"
	
	_url = URL
	
	if _url.strip() == "":
		_url = _dataURL
		
	try:
		# open a file to write the content into
		_fd = open(fileName,"w")

		# read the lines and write into the file
		for line in urllib2.urlopen(_url):
			_fd.write(line)
			
	except:
		# download failed, remove the empty file
		os.remove(fileName)
		
		# return the error to calling logic
		raise
		
	finally:
		# close the output file
		_fd.close()
	
if __name__ == "__main__":
	downloadFile()