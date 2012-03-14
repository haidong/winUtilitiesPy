import argparse
from winUtility import getServiceState

parser = argparse.ArgumentParser(description='Get service status')
parser.add_argument('-f', '--fileInput', help='The presence of this parameter indicates server names come from a file',  action='store_true', default=False, dest='fileInput')
parser.add_argument('-i', '--input', help='When -f is present, please provide the name of the file that contains a list of servers, each on its own line. Otherwise, please type a list of servers, separated by comma.',  required=True, dest='iInput')
parser.add_argument('-u', '--user', help='Please provide the user account, in the form of domain\\login',  default = None, dest='uUser')
parser.add_argument('-p', '--password', help='Please provide the password for Alex 0 account',  default = None, dest='pPassword')
parser.add_argument('-s', '--service', help='Please provide the name of the service',  required = True, dest='sService')

argList = parser.parse_args()

if argList.fileInput:
	text_file = open("%s" % argList.iInput, "r")
	serverList = text_file.readlines()
else:
	serverList = argList.iInput.split(',')

print argList.uUser
serviceStatus = {}
for server in serverList:
	serviceStatus[server.strip()] = getServiceState(argList.sService, server.strip(), argList.uUser, argList.pPassword)

print serviceStatus
