import unittest
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'winUtility'))
import winUtility

class winUtilityTest(unittest.TestCase):

	def test_runCmd_dir_stdErr(self):
		returnCode, stdOut, stdErr = winUtility.runCmd("dir")
		self.assertEqual(stdErr, '')
	def test_runCmd_dir_stdOut(self):
		returnCode, stdOut, stdErr = winUtility.runCmd("dir")
		self.assertIn("winUtility_test.py", stdOut)


	def test_getServiceStartupAccount_dhcp(self):
		self.assertEqual(winUtility.getServiceStartupAccount('Dhcp', 'LocalHost'), 'NT Authority\\LocalService')
	def test_getServiceStartupAccount_junk(self):
		self.assertEqual(winUtility.getServiceStartupAccount('junk', 'LocalHost'), None)
	#@unittest.skip("don't run this one if you don't have a named instance called MSSQL$SQLEXPRESS with Network Service as its startup account")
	def test_getServiceStartupAccount_namedInstance(self):
		self.assertEqual(winUtility.getServiceStartupAccount('MSSQL$SQLEXPRESS', 'LocalHost').upper(), 'NT AUTHORITY\\NETWORK SERVICE')

	def test_getServiceStartupType_dhcp(self):
		self.assertEqual(winUtility.getServiceStartupType('Dhcp', 'LocalHost'), 'AUTO_START')
	def test_getServiceStartupType_junk(self):
		self.assertEqual(winUtility.getServiceStartupType('junk', 'LocalHost'), None)
	#@unittest.skip("don't run this one if you don't have a named instance called MSSQL$SQLEXPRESS with Network Service as its startup account")
	def test_getServiceStartupType_namedInstance(self):
		self.assertEqual(winUtility.getServiceStartupType('MSSQL$SQLEXPRESS', 'LocalHost').upper(), 'AUTO_START')

	def test_getServiceState_dhcp(self):
		self.assertEqual(winUtility.getServiceState('Dhcp', 'LocalHost'), 'RUNNING')
	def test_getServiceState_junk(self):
		self.assertEqual(winUtility.getServiceState('junk', 'LocalHost'), None)
	#@unittest.skip("don't run this one if you don't have a named instance called MSSQL$SQLEXPRESS")
	def test_getServiceState_namedInstance(self):
		self.assertEqual(winUtility.getServiceState('MSSQL$SQLEXPRESS', 'LocalHost').upper(), 'RUNNING')


	def test_setServiceStatus_ALG(self):
		self.assertTrue(winUtility.setServiceStatus('ALG', 'LocalHost', 'stop'))
		self.assertEqual(winUtility.getServiceState('ALG', 'LocalHost'), 'STOPPED')
		self.assertTrue(winUtility.setServiceStatus('ALG', 'LocalHost', 'start'))
		self.assertTrue(winUtility.setServiceStatus('ALG', 'LocalHost', 'start'))
		self.assertEqual(winUtility.getServiceState('ALG', 'LocalHost'), 'RUNNING')
		self.assertTrue(winUtility.setServiceStatus('ALG', 'LocalHost', 'restart'))
		self.assertEqual(winUtility.getServiceState('ALG', 'LocalHost'), 'RUNNING')
		self.assertTrue(winUtility.setServiceStatus('ALG', 'LocalHost', 'stop'))
		self.assertEqual(winUtility.getServiceState('ALG', 'LocalHost'), 'STOPPED')


	def test_setServiceStartupType_ALG(self):
		self.assertTrue(winUtility.setServiceStartupType('ALG', 'LocalHost', 'auto'))
		self.assertFalse(winUtility.setServiceStartupType('ALG', 'LocalHost', 'junk'))
		self.assertEqual(winUtility.getServiceStartupType('ALG', 'LocalHost'), 'AUTO_START (DELAYED)')
		self.assertTrue(winUtility.setServiceStartupType('ALG', 'LocalHost', 'manual'))
		self.assertEqual(winUtility.getServiceStartupType('ALG', 'LocalHost'), 'DEMAND_START')
		self.assertTrue(winUtility.setServiceStartupType('ALG', 'LocalHost', 'disabled'))
		self.assertEqual(winUtility.getServiceStartupType('ALG', 'LocalHost'), 'DISABLED')
		self.assertTrue(winUtility.setServiceStartupType('ALG', 'LocalHost', 'automatic'))
		self.assertEqual(winUtility.getServiceStartupType('ALG', 'LocalHost'), 'AUTO_START (DELAYED)')
		self.assertTrue(winUtility.setServiceStartupType('ALG', 'LocalHost', 'manual'))


	def test_getDiskVolumeInfo(self):
		self.assertEqual(winUtility.getDiskVolumeInfo('LocalHost')[0]['driveLetter'], 'C')
		self.assertEqual(winUtility.getDiskVolumeInfo('junk'), None)
