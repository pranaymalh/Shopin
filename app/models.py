from app import db
from werkzeug.security import generate_password_hash,check_password_hash

class User(db.Document):
	user_id=db.IntField(unique=True)
	first_name=db.StringField(max_length=50)
	last_name=db.StringField(max_length=50)
	email=db.StringField(unique=True,max_length=50)
	password=db.StringField(max_length=120)
	def set_password(self,password):
		self.password=generate_password_hash(password)		
	def get_password(self,password):
		return check_password_hash(self.password,password)

class Item(db.Document):
	item_id=db.IntField(unique=True)
	item_name=db.StringField(max_length=100)
	item_img_address=db.StringField(max_length=500)
	price=db.IntField(default=0)

class Cart(db.Document):
	cart_id=db.StringField(unique=True)
	user_id=db.IntField()
	item_id=db.IntField()
	count=db.IntField()

class Order(db.Document):
	order_id=db.StringField(unique=True)
	user_id=db.IntField()
	order_items=db.ListField()
	order_total=db.IntField()
	ship_add=db.StringField(max_length=100)