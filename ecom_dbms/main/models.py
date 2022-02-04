from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
	#cust_id= models.AutoField(verbose_name= "Customer ID", primary_key = True)
	user= models.OneToOneField(User, null= True, blank= True, on_delete=models.CASCADE)
	first_name= models.CharField(verbose_name= "First Name", max_length=150, null=True)
	last_name= models.CharField(verbose_name= "Last Name", max_length=150, null=True)
	date_of_birth= models.DateTimeField(verbose_name="Date of Birth", null= True)
	
	#age
	def get_age(self):
		age = datetime.date.today()-self.birth_date
		return int((age).days/365.25)

	GENDER_CHOICES=(
    	("Male", "Male"),
    	("Female", "Female"),
    	("OtherD", "Other"),
    	)
	gender= models.CharField(max_length=7, choices= GENDER_CHOICES, default='Male')


class Product(models.Model):
	#product_id= models.AutoField(verbose_name= "Product ID", primary_key= True)
	title= models.CharField(verbose_name= "Title", max_length= 30)
	image= models.ImageField(verbose_name= 'Product Image',upload_to= 'media', null=True, blank=True) #upload to media folder
	description= models.CharField(verbose_name= "Description", max_length= 250)
	price= models.DecimalField(verbose_name= "Price", decimal_places=2, max_digits= 6)
	date= models.DateTimeField(auto_now_add= True)

	def _str__(self):
		return self.title

	@property
	def imageURL(self):
		try:
			url= self.image.url
		except:
			url = ''
		return url

class Order(models.Model):
	#order_no= models.AutoField(verbose_name= "Order No", primary_key= True)
	customer= models.ForeignKey(Customer, on_delete=models.SET_NULL, blank= True, null=True)
	date= models.DateTimeField(auto_now_add= True)
	complete= models.BooleanField(default= False, null= True, blank= False)
	transaction_id= models.IntegerField( null= True)

	@property
	def shipping(self):
		shipping = True
		orderitems = self.orderitem_set.all()
		for i in orderitems:
			shipping = True
		return shipping

	@property
	#Total cart value, that's why for loop! :D (which is why created get_total first)
	def get_cart_total(self):
		orderitems= self.orderitem_set.all()
		total= sum([item.get_total for item in orderitems])
		return total

	#total quantity
	@property
	def get_cart_items(self):
		orderitems= self.orderitem_set.all()
		total= sum([item.quantity for item in orderitems])
		return total

class OrderItem(models.Model):
	product= models.ForeignKey(Product, on_delete= models.SET_NULL, blank=True, null=True)
	#single order can have multiple order items
	order= models.ForeignKey(Order, on_delete= models.SET_NULL, blank=True, null=True)
	quantity= models.IntegerField(default=0, null=True, blank=True)
	date= models.DateTimeField(auto_now_add= True)

	#To render total
	@property
	def get_total(self):
		#product consists price
		total= self.quantity * self.product.price
		return total

class Address(models.Model):
	#even if order gets deleted by reason x, would like to have the shipping address of the customer
	customer= models.ForeignKey(Customer, on_delete= models.SET_NULL, blank=True, null=True)
	order=models.ForeignKey(Order, on_delete= models.SET_NULL, blank=True, null=True)
	
	house_No= models.CharField(verbose_name= "House No", max_length= 200, null= True)
	street= models.CharField(verbose_name= "Street",max_length= 200, null= True)
	locality= models.CharField(verbose_name= "Locality",max_length= 200, null= True)
	landmark= models.CharField(verbose_name= "Landmark",max_length= 200, null= True)
	city= models.CharField(verbose_name= "City", max_length=200, null= True)
	state= models.CharField(verbose_name= "State",max_length= 200, null= True)
	zipcode= models.CharField(verbose_name= "Zipcode",max_length=200, null= True)
	date_added= models.DateTimeField(auto_now_add= True)

	def __str__(self):
		return self.city