from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import * 
from django.forms.widgets import DateInput

#Updated User creation form
class NewUserForm(UserCreationForm):
	email= forms.EmailField(required= True)

	class Meta:
		model= User
		fields= ("username", "email", "password1", "password2")

	def save(self, commit= True):
		user= super(NewUserForm, self).save(commit= False) #dont save it 
		user.email= self.cleaned_data['email'] #modify and then save
		if commit:
			user.save()
		return user

#customer form for front end 
class CustomerForm(forms.ModelForm):
	YEARS= [x for x in range(1955,2010)]
	date_of_birth= forms.DateField(initial="2000-01-01", widget=forms.SelectDateWidget(years= YEARS))

	class Meta:
		model= Customer
		fields= ("first_name", "last_name", "date_of_birth", "gender")

		
