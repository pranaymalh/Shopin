from flask import url_for,render_template,redirect,session,flash
from app import app
from app.forms import LoginForm,RegisterForm,AddItemForm,PlaceOrderForm
from app.models import User,Item,Cart,Order
import uuid
l=["https://cdn.pixabay.com/photo/2017/11/26/16/36/landscape-2979296_1280.jpg","https://cdn.pixabay.com/photo/2018/04/22/10/52/nature-3340709_1280.jpg"]
@app.route("/")
@app.route("/index")
def index():
	items=Item.objects().all()
	return render_template('index.html',items=items,l=l)

@app.route("/checkout",methods=["GET","POST"])
def checkout():
	form=PlaceOrderForm()
	classes=list(User.objects.aggregate(*[
    {
        '$lookup': {
            'from': 'cart', 
            'localField': 'user_id', 
            'foreignField': 'user_id', 
            'as': 'r1'
        }
    }, {
        '$unwind': {
            'path': '$r1', 
            'includeArrayIndex': 'r1_id', 
            'preserveNullAndEmptyArrays': False
        }
    }, {
        '$lookup': {
            'from': 'item', 
            'localField': 'r1.item_id', 
            'foreignField': 'item_id', 
            'as': 'r2'
        }
    }, {
        '$unwind': {
            'path': '$r2', 
            'preserveNullAndEmptyArrays': False
        }
    }, {
        '$match': {
            'user_id': session["user_id"]
        }
    }, {
        '$sort': {
            'item_id': 1
        }
    }
]))
	if len(classes)==0:
		flash(f"Cart is Empty","danger")
		return redirect("/cart")
	summed=0
	for i in classes:
		summed+=i['r2']['price']*i['r1']['count']
	if form.validate_on_submit():
		id=uuid.uuid4()
		order_id=str(id.int)
		while Order.objects(order_id=order_id).first():
			id=uuid.uuid4()
			order_id=str(id.int)
		user_id=session["user_id"]
		order_items=classes
		order_total=summed
		ship_add=form.ship_add.data
		Order(order_id=order_id,user_id=session["user_id"],order_items=order_items,order_total=order_total,ship_add=ship_add).save()
		for cart in Cart.objects(user_id=session["user_id"]).all():
			Cart.objects(cart_id=cart.cart_id).delete()
		flash(f"Order placed successfully!","success")
		return redirect(url_for('orders'))
	return render_template("checkout.html",classes=classes,summed=summed,form=form)

@app.route("/orders")
def orders():
	if not session.get("username"):
		return redirect(url_for('login'))
	all_orders=Order.objects(user_id=session['user_id']).all()
	return render_template("orders.html",all_orders=all_orders)

@app.route("/upcount/<idx>")
def upcount(idx):
	cart=Cart.objects(cart_id=idx).first()
	counter=cart.count+1
	cart.update(count=counter)
	return redirect(url_for('cart'))

@app.route("/downcount/<idx>")
def downcount(idx):
	cart=Cart.objects(cart_id=idx).first()
	if cart.count==1:
		Cart.objects(cart_id=idx).delete()
	else:	
		counter=cart.count-1
		cart.update(count=counter)
	return redirect(url_for('cart'))

@app.route("/remove/<idx>")
def remove(idx):
	if Cart.objects(cart_id=idx).first().count>1:
		cart=Cart.objects(cart_id=idx).first()
		counter=cart.count-1
		cart.update(count=counter)
	else:
		Cart.objects(cart_id=idx).delete()
	return redirect(url_for('cart'))

@app.route("/logout")
def logout():
	session["user_id"]=False
	session.pop("username",None)
	session.pop("email",None)
	return redirect(url_for('login'))

@app.route("/login",methods=["GET","POST"])
def login():
	if session.get("username"):
		return redirect(url_for('index'))
	form=LoginForm()
	if form.validate_on_submit():
		email=form.email.data
		password=form.password.data
		user=User.objects(email=email).first()
		if user and user.get_password(password):
			session["user_id"]=user.user_id
			session["username"]=user.first_name
			session["email"]=user.email
			flash(f"User logged in successfully","success")
			return redirect(url_for('index'))
		flash(f"Something went wrong","danger")
	return render_template('login.html',form=form)

@app.route("/register",methods=["GET","POST"])
def register():
	if session.get("username"):
		return redirect(url_for('index'))
	form=RegisterForm()
	if form.validate_on_submit():
		user_id=User.objects().count()
		user_id+=1
		first_name=form.first_name.data
		last_name=form.last_name.data
		email=form.email.data
		password=form.password.data
		user=User(user_id=user_id,email=email,first_name=first_name,last_name=last_name)
		user.set_password(password)
		user.save()
		flash(f"User registered successfully","success")
		return redirect(url_for('login'))
	return render_template('register.html',form=form)

@app.route("/additem",methods=["GET","POST"])
def additem():
	form=AddItemForm()
	if form.validate_on_submit():
		item_id=Item.objects().count()
		item_id+=1
		item_name=form.item_name.data
		item_img_address=form.item_img_address.data
		price=form.price.data
		Item(item_id=item_id,item_name=item_name,item_img_address=item_img_address,price=price).save()
		flash(f"Item added successfully","success")
		return redirect(url_for('additem'))
	return render_template('additem.html',form=form)

@app.route("/addcart/<idx>")
def addcart(idx):
	if not session.get("username"):
		return redirect(url_for('login'))
	carts=Cart.objects(item_id=idx).all()
	for cart in carts:
		if cart and cart.user_id==session["user_id"]:
			counter=cart.count+1
			cart.update(count=counter)			
			flash(f"Item added to cart successfully","success")
			return redirect(url_for('index'))
	id=uuid.uuid4()
	cart_id=str(id.int)
	while Cart.objects(cart_id=cart_id).first():
		id=uuid.uuid4()
		cart_id=str(id.int)
	user_id=session["user_id"]
	item_id=idx
	Cart(cart_id=cart_id,user_id=user_id,item_id=item_id,count=1).save()
	flash(f"Item added to cart successfully","success")
	return redirect(url_for('index'))


@app.route("/cart")
def cart():
	if not session.get("username"):
		return redirect(url_for('login'))
	classes=list(User.objects.aggregate(*[
    {
        '$lookup': {
            'from': 'cart', 
            'localField': 'user_id', 
            'foreignField': 'user_id', 
            'as': 'r1'
        }
    }, {
        '$unwind': {
            'path': '$r1', 
            'includeArrayIndex': 'r1_id', 
            'preserveNullAndEmptyArrays': False
        }
    }, {
        '$lookup': {
            'from': 'item', 
            'localField': 'r1.item_id', 
            'foreignField': 'item_id', 
            'as': 'r2'
        }
    }, {
        '$unwind': {
            'path': '$r2', 
            'preserveNullAndEmptyArrays': False
        }
    }, {
        '$match': {
            'user_id': session["user_id"]
        }
    }, {
        '$sort': {
            'item_id': 1
        }
    }
]))
	return render_template('cart.html',classes=classes,upcount=upcount,downcount=downcount)