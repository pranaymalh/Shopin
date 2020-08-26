from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,IntegerField
from wtforms.validators import Email,Length,EqualTo,DataRequired

class LoginForm(FlaskForm):
	email=StringField("Email",validators=[DataRequired(),Email()])
	password=PasswordField("Password",validators=[DataRequired()])
	submit=SubmitField("Login")

class RegisterForm(FlaskForm):
	first_name=StringField("First Name",validators=[DataRequired(),Length(min=2,max=50)])
	last_name=StringField("Last Name",validators=[DataRequired(),Length(min=2,max=50)])
	email=StringField("Email",validators=[DataRequired(),Email()])
	password=PasswordField("Password",validators=[DataRequired(),Length(min=6,max=50)])
	confirm_password=PasswordField("Confirm Password",validators=[DataRequired(),Length(min=6,max=50),EqualTo('password')])
	submit=SubmitField("Register")

class AddItemForm(FlaskForm):
	item_name=StringField("Item Name : ",validators=[DataRequired(),Length(min=10,max=100)])
	item_img_address=StringField("Image Link : ",validators=[DataRequired(),Length(max=500)])
	price=IntegerField("Price : ",validators=[DataRequired()])
	submit=SubmitField("Add Item")

class PlaceOrderForm(FlaskForm):
	ship_add=StringField("Enter Shipping Address : ",validators=[DataRequired()])
	submit=SubmitField("Place Order")