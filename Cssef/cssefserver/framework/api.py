from __future__ import absolute_import
from cssefserver.framework import CssefCeleryApp
from cssefserver.framework import dbPath
from cssefserver.framework.utils import getEmptyReturnDict
from cssefserver.framework.utils import databaseConnection
from cssefserver.modules.account import User
from cssefserver.modules.account.api import organizationEndpointsDict as organizationEndpoints
from cssefserver.modules.account.api import userEndpointsDict as userEndpoints
from cssefserver.modules.competition.api import endpointsDict as competitionEndpoints

@CssefCeleryApp.task(name = 'availableEndpoints')
def availableEndpoints():
	returnDict = getEmptyReturnDict()
	returnDict['content'] = [
		endpointsDict,
		userEndpoints,
		organizationEndpoints,
		competitionEndpoints
	]
	return returnDict

@CssefCeleryApp.task(name = 'login')
def login(username, password):
	db = databaseConnection(dbPath)
	user = User.search(db, username = username)
	print user
	token = user[0].authenticatePassword(password)
	returnDict = getEmptyReturnDict()
	if not token:
		returnDict['message'] = ["Incorrect username or password."]
		returnDict['value'] = 1
	else:
		returnDict['content'] = token
	return returnDict

endpointsDict = {
	"name": "Framework",
	"author": "",
	"menuName": "framework",
	"endpoints": []
}