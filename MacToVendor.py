import urllib2, logging, sys, re

FORMAT = '%(asctime)-15s %(user)-8s %(message)s'
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

# ---------------------------------
class MacVendorData:

	MacAddress = []
	VendorData = []
	
	def __init__(self):
		logger = logging.getLogger("MacVendorData")
	
	def addDetails(self, data):
		#logging.debug("addDetails()")
		#logging.debug(data)
		
		p = re.compile("[\s#]+")
		#print p.split(data,2)
		
		
		mac, vendorS, vendorL = p.split(data,2)
		
		#logging.debug("MacAddress: "+mac)
		#logging.debug("Vendor: "+vendorS + "#" + vendorL)
		
		
		self.MacAddress.append(mac)
		self.VendorData.append(vendorS + "#" + vendorL)
		
		
	def getDetails(self,key):
		index = self.MacAddress.index(key)
		return self.VendorData[index]
		
	
	
	
# -----------------------------------
class MacToVendor:
	'''
	Data Source
	https://code.wireshark.org/review/gitweb?p=wireshark.git;a=blob_plain;f=manuf;hb=HEAD

	Data Format
	00:00:01	XeroxCor               # XEROX CORPORATION
	'''

	_dataURL = "https://code.wireshark.org/review/gitweb?p=wireshark.git;a=blob_plain;f=manuf;hb=HEAD"
	_fileName = "manuf.txt"
	_mvd = MacVendorData()
	
	logger = logging.getLogger("MacToVendor")
	
	def __init__(self):
		'''
		Read the Data Source and prepare the table.
		XXX: Need to find the best way to optimize for single and multiple
		     query.
		'''
		logging.info("Initializing")
		
		fd = open(self._fileName,"r")
		
		#for line in urllib2.urlopen(self.dataURL):
		for line in fd:
			#logging.debug(len(line))
			#logging.debug(line)
			
			if line.strip() == '':
				pass
			elif (line[0][0] != "#"):
				#logging.debug(line)
				self._mvd.addDetails(lineData)
		
		
	def getVendorShort(self,key):
		'''
		Returns the short name of the Vendor.
		'''
		return self._mvd.getDetails(key).split("#")[0]
		
	def getVendorFull(self,key):
		'''
		Returns the full name of the Vendor.
		'''
		return self._mvd.getDetails(key).split("#")[1]


mtv = MacToVendor()
print mtv.getVendorShort("00:00:00")
print mtv.getVendorFull("00:00:00")

print mtv.getVendorShort("00:00:0F")
print mtv.getVendorFull("00:00:0F")
