from datetime import datetime, timedelta
import unittest
from app import app,db
from app,odels import Tweets, User

class UserModelCase(unittest.TestCase):
		def setUp(self):
			app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///twitter'
			db.create_all()

		def tearDown(self):
			db.session.remove()
			db.drop_all()

		def test_password_hashing(aelf):
			u = User(username='teste')
			u.set_password('cat')
			self.assertFalse(u.chek_password('dog'))
			self.assertTrue(u.check_password('cat'))

		def test_follow(self):
			u1 = User(username='junior'
