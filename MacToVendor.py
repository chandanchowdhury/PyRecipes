"""
Download data from WireShark Mac Address repository and save in a file. Then later 
use the file to return the Vendor details for a Mac address.

Data Source:
https://code.wireshark.org/review/gitweb?p=wireshark.git;a=blob_plain;f=manuf;hb=HEAD
"""
import DownloadURLText, urllib2, logging, sys, re

FORMAT = "%(asctime)s - %(levelname)s - %(module)s(%(lineno)d) - %(message)s"
#TODO: Why the formatter does not work?
#logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
# XXX: Formatting now working.
logging.basicConfig(stream=sys.stderr, level=logging.INFO, format=FORMAT)

# ---------------------------------
class MacVendorData:
	"""
	Purpose: Give it a line via addDetails() and it will parse the line and save in 
	internal List to return later.

	Data Format  - OUI
	00:00:01	XeroxCor               # XEROX CORPORATION
	
	Ref: http://en.wikipedia.org/wiki/Organizationally_unique_identifier

	
	TODO: Currently for IABs it require the full Mac address part.
	Data Format - IAB
	00:50:C2:00:30:00/36	Microsof               # Microsoft
	
	Ref: http://en.wikipedia.org/wiki/Individual_Address_Block
	"""

	_MacAddress = []
	_VendorData = []
	
	_logger = ""
	
	def __init__(self):
		self._logger = logging.getLogger()
	
	def addDetails(self, data):
		"""
		Save a Mac address and corresponding Vendor detail in internal list.
		"""
		self._logger.debug("addDetails()")
		self._logger.debug(data)
		
		# prepare the regular expression to split the record.
		p = re.compile("[\s#]+")
		
		# no more than 3 splits i.e. anything after second word keep them together.
		mac, vendorS, vendorL = p.split(data,2)
		
		self._logger.debug("MacAddress: "+mac)
		self._logger.debug("Vendor: "+vendorS + "#" + vendorL)
		
		
		self._MacAddress.append(mac)
		self._VendorData.append(vendorS + "#" + vendorL)
		
		
	def getDetails(self,key):
		"""
		Returns the Vendor details.
		The Short and Long description are separated by hash, caller need to split
		and use accordingly.
		"""
		try:
			# find the key of Mac address
			index = self._MacAddress.index(key)
			# return the Vendor data for the corresponding index
			return self._VendorData[index]
		except ValueError:
			self._logger.warning("Key Not Found: " + key)
			return "<Not Found>#<Mac Address Not Found>"
		
# -----------------------------------
class MacToVendor:
	"""
		Read the MAC data from either file and use MacVendorData to store the details.

		If file is not available, try to download the data.
	"""

	_dataURL = "https://code.wireshark.org/review/gitweb?p=wireshark.git;a=blob_plain;f=manuf;hb=HEAD"
	_fileName = "manuf.txt"
	
	_mvd = MacVendorData()
	_fileD = ""
	
	_logger = logging.getLogger()
	
	def __init__(self):
		"""
		Read the Data Source and prepare the table.
		TODO: Need to find the best way to optimize for single and multiple
		     query.
		"""
		self._logger.info("Initializing...")
		
		try:
			# open the input Mac data file.
			_fileD = open(self._fileName,"r")
			
			# TODO: Check for empty file and force download if so.
			
		except IOError as ioe:
			self._logger.warning("MAC Data file not already downloaded...")
		
			# try downloding the data
			try:
				self._logger.info("Trying to download MAC data...")
				DownloadURLText.downloadFile(self._dataURL,self._fileName)
				self._logger.info("Download data complete...")
				
			except:
				self._logger.critical("Download data FAILED...")
				# magic
				self._logger.critical(sys.exc_info()[1])
				# download failed, no need to continue
				self._logger.info("Biday nisthur prithibi...")
				exit(1)
			
		# try again after data is downloaded
		try:
			_fileD = open(self._fileName,"r")
			
			for line in _fileD:
				self._logger.debug(line)
			
				# skip empty lines
				if line.strip() == "":
					pass
				# skip lines starting with hash as they are comments
				elif (line[0][0] != "#"):
					self._logger.debug(line)
					self._mvd.addDetails(line)
			
		except IOError as ioe:
			self._logger.warning("MAC Data file not available...")
			self._logger.error(ioe)
			# data is not available, no need to continue
			self._logger.info("Biday nisthur prithibi...")
			exit(2)
		
		
		
		
	def getVendorShort(self,key):
		"""
		Returns the short name of the Vendor.
		"""
		return self._mvd.getDetails(key).split("#")[0]
		
	def getVendorFull(self,key):
		"""
		Returns the full name of the Vendor.
		"""
		return self._mvd.getDetails(key).split("#")[1]

# run only when used standalone, helps in importing by other modules.
if __name__ == "__main__":
	mtv = MacToVendor()
	print mtv.getVendorShort("00:00:00")
	print mtv.getVendorFull("00:00:00")

	print mtv.getVendorShort("00:00:0F")
	print mtv.getVendorFull("00:00:0F")

	print mtv.getVendorShort("00:50:C2")
	print mtv.getVendorShort("00:50:C2:00:30:00/36")