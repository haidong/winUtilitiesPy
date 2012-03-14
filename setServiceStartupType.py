import argparse
from winUtility import setServiceStartupType

parser = argparse.ArgumentParser(description='Get service status')
parser.add_argument('-f', '--fileInput', help='The presence of this parameter indicates server names come from a file',  action='store_true', default=False, dest='fileInput')
parser.add_argument('-i', '--input', help='When -f is present, please provide the name of the file that contains a list of servers, each on its own line. Otherwise, please type a list of servers, separated by comma.',  required=True, dest='iInput')
parser.add_argument('-s', '--service', help='Please provide the name of the service',  required = True, dest='sService')
parser.add_argument('-t', '--type', help='Please provide the type name [manual|auto|disabled]',  required = True, dest='tType')

argList = parser.parse_args()

if argList.fileInput:
	text_file = open("%s" % argList.iInput, "r")
	serverList = text_file.readlines()
else:
	serverList = argList.iInput.split(',')

startType = {}
for server in serverList:
	startType[server.strip()] = setServiceStartupType(argList.sService, server.strip(), argList.tType)

print startType
