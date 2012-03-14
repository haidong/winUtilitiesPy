import re, subprocess
from datetime import datetime

"""Haidong's class of Windows-specific utilities. It uses sysinternal tools fairly extensively. This is written mostly for SQL Server administration"""

def runCmd(cmd):
	proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	out, err = proc.communicate()
	ret = proc.returncode
	return (ret, out, err)

def getServiceStartupAccount(service, server, login=None, password=None):
	"""Getting service startup account by parsing results from
	psservice \\server config
	SQL Server named instance has $ in its name, which needs to be escaped during regex search. Ditto for server names with dot or space in them"""
	if login is None:
		cmd = """psservice \\\\%s config""" % server.strip()
	else:
		cmd = """psservice \\\\%s -u "%s" -p "%s" config""" % (server.strip(), login, password)

	returnCode, stdOut, stdErr = runCmd(cmd)
	targetServiceFound = False

	service = service.replace('$', '\$')
	service = service.replace('.', '\.')
	service = service.replace(' ', '\ ')
	serviceName = re.compile(r'SERVICE_NAME:\s%s.*$' % service, re.IGNORECASE)
	startupAccount = re.compile(r'\tSERVICE_START_NAME:\s(.+)')

	for line in stdOut.split('\n'):
		if targetServiceFound:
			reResult = startupAccount.search(line)
			if reResult:
				return reResult.group(1).strip()
		else:
			reResult = serviceName.search(line)
			if reResult:
				targetServiceFound = True
	
	if not targetServiceFound:
		return None

def getServiceState(service, server, login=None, password=None):
	"""Getting service status by parsing results from
	psservice \\server query service
	SQL Server named instance has $ in its name, which needs to be escaped during regex search. Ditto for server names with dot or space in them
	Note that the command string is built before compiling the regex. Regex needs proper escape, but psservice query can take $ signs. I haven't tested if psservice can take space and/or dot in the query command"""
	
	if login is None:
		cmd = """psservice \\\\%s query %s""" % (server.strip(), service)
	else:
		cmd = """psservice \\\\%s -u "%s" -p "%s" query %s""" % (server.strip(), login, password, service)

	returnCode, stdOut, stdErr = runCmd(cmd)
	targetServiceFound = False

	service = service.replace('$', '\$')
	service = service.replace('.', '\.')
	service = service.replace(' ', '\ ')
	serviceName = re.compile(r'SERVICE_NAME:\s%s.*$' % service, re.IGNORECASE)
	serviceState = re.compile(r'\tSTATE\s+:\s(.+)')

	for line in stdOut.split('\n'):
		if targetServiceFound:
			reResult = serviceState.search(line)
			if reResult:
				return reResult.group(1).partition('  ')[2].strip()
		else:
			reResult = serviceName.search(line)
			if reResult:
				targetServiceFound = True
	
	if not targetServiceFound:
		return None

def setServiceStatus(service, server, action, login=None, password=None):
	"""Change service status by running
	psservice \\server [stop|start|restart] service
	"""	
	if login is None:
		cmd = """psservice \\\\%s %s %s""" % (server.strip(), action, service)
	else:
		cmd = """psservice \\\\%s -u "%s" -p "%s" %s %s""" % (server.strip(), login, password, action, service)

	returnCode, stdOut, stdErr = runCmd(cmd)

	time1 = datetime.now()

	while (datetime.now() - time1).seconds < 30:
		status = getServiceState(service, server, login, password)
		if action.upper() == 'STOP':
			return True
		elif (action.upper() == 'START') or (action.upper() == 'RESTART'):
			return True
		else:
			return False

def getServiceStartupType(service, server, login=None, password=None):
	"""Getting service startup type by parsing results from
	psservice \\server config
	SQL Server named instance has $ in its name, which needs to be escaped during regex search. Ditto for server names with dot or space in them"""
	if login is None:
		cmd = """psservice \\\\%s config""" % server.strip()
	else:
		cmd = """psservice \\\\%s -u "%s" -p "%s" config""" % (server.strip(), login, password)

	returnCode, stdOut, stdErr = runCmd(cmd)
	targetServiceFound = False

	service = service.replace('$', '\$')
	service = service.replace('.', '\.')
	service = service.replace(' ', '\ ')
	serviceName = re.compile(r'SERVICE_NAME:\s%s.*$' % service, re.IGNORECASE)
	startupType = re.compile(r'\tSTART_TYPE\s+:\s(.+)')

	for line in stdOut.split('\n'):
		if targetServiceFound:
			reResult = startupType.search(line)
			if reResult:
				return reResult.group(1).partition('  ')[2].strip()
		else:
			reResult = serviceName.search(line)
			if reResult:
				targetServiceFound = True
	
	if not targetServiceFound:
		return None

def setServiceStartupType(service, server, startupType, login=None, password=None):
	"""Changing service startup type by running:
	psservice \\server setconfig
	"""
	if startupType.lower() == 'manual':
		startupType = 'demand'
	elif startupType.lower() == 'automatic':
		startupType = 'auto'
	elif startupType.lower() == 'disable':
		startupType = 'disabled'

	if login is None:
		cmd = """psservice \\\\%s setconfig %s %s""" % (server.strip(), service.strip(), startupType.strip())
	else:
		cmd = """psservice \\\\%s -u "%s" -p "%s" setconfig %s %s """ % (server.strip(), login, password, service.strip(), startupType.strip())

	returnCode, stdOut, stdErr = runCmd(cmd)

	setResult = getServiceStartupType(service, server, login, password)

	if startupType == 'demand':
		if setResult == 'DEMAND_START':
			return True
	elif startupType == 'auto':
		if setResult == 'AUTO_START (DELAYED)':
			return True
	elif startupType == 'disabled':
		if setResult == 'DISABLED':
			return True
	
	return False
