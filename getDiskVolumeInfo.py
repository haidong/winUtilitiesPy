import argparse
from winUtility import getDiskVolumeInfo

parser = argparse.ArgumentParser(description='Get server disk volume total size and available space')
parser.add_argument('-f', '--fileInput', help='The presence of this parameter indicates server names come from a file',  action='store_true', default=False, dest='fileInput')
parser.add_argument('-i', '--input', help='When -f is present, please provide the name of the file that contains a list of servers, each on its own line. Otherwise, please type a list of servers, separated by comma.',  required=True, dest='iInput')

argList = parser.parse_args()

if argList.fileInput:
	text_file = open("%s" % argList.iInput, "r")
	serverList = text_file.readlines()
else:
	serverList = argList.iInput.split(',')

for server in serverList:
	diskInfo = getDiskVolumeInfo(server.strip())
	#header = server.strip()
	#line = server.strip()
	#for disk in diskInfo:
		#header = header + ',' + disk['driveLetter'] + ' totalSize,' + disk['driveLetter'] + ' availableSize,freePercentage'
	#print header
	#for disk in diskInfo:
		#line = line + ',' + disk['totalSize'] + ',' + disk['availableSize'] + ',' + disk['percentFree']
	#print line
