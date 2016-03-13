import bcrypt
from cssefserver.framework import dbPath
from cssefserver.framework.utils import returnError
from cssefserver.framework.utils import databaseConnection
import cssefserver.modules.account

class PasswordHash(object):
	"""
	This code pulled from http://variable-scope.com/posts/storing-and-verifying-passwords-with-sqlalchemy
	There are a couple minor changes to it, but most credit goes Elmer de Looff - Thank you!
	"""
	def __init__(self, hash_):
		"""Instantiates a PasswordHash object based on a provided string representing a bcrypt hash.

		Args:
			hash_ (str): The hash string to build the object off of.

		Raises:
			Assertion Error: If `hash_` is not of length 60.

			Assertion Error: If `hash_` does not contain three '$'.
		"""
		assert len(hash_) == 60, 'bcrypt hash should be 60 chars.'
		assert hash_.count('$'), 'bcrypt hash should have 3x "$".'
		self.hash = str(hash_)
		self.rounds = int(self.hash.split('$')[2])

	def __eq__(self, candidate):
		"""Hashes the candidate string and compares it to the stored hash."""
		if isinstance(candidate, basestring):
			if isinstance(candidate, unicode):
				candidate = candidate.encode('utf8')
			return bcrypt.hashpw(candidate, self.hash) == self.hash
		return False

	def __repr__(self):
		"""Simple object representation."""
		return self.hash

	@classmethod
	def new(cls, password, rounds):
		"""Creates a PasswordHash from the given password."""
		if isinstance(password, unicode):
			password = password.encode('utf8')
		return cls(bcrypt.hashpw(password, bcrypt.gensalt(rounds)))

def authorizeAccess(authDict):
	db = databaseConnection(dbPath)
	# Importing for this got pretty ugly... :(
	userList = cssefserver.modules.account.User.search(db, username = authDict['username'], organization = authDict['organization'])
	if len(userList) < 1:
		# No matching user was found
		return returnError('user_not_found')
	if len(userList) > 1:
		# There are multiple users. This is extremely bad
		return returnError('multiple_users_found')
	user = userList[0]
	# Authenticate the user
	if not user.authenticate(authDict):
		return returnError('user_auth_failed')
	# Authorize the user
	if not user.authorized(authDict, 'organization'):
		return returnError('user_permission_denied')
	return None
