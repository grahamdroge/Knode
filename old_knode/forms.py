from django import forms 
from django.forms import ModelForm
from .models import Interests, UserProfile, Tools, Posts
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class TopicForm(forms.Form):

	health = forms.BooleanField(required=False)
	finance = forms.BooleanField(required=False)
	auto = forms.BooleanField(required=False)
	film = forms.BooleanField(required=False)
	entrepreneurship = forms.BooleanField(required=False)
	sports = forms.BooleanField(required=False)
	books = forms.BooleanField(required=False)
	politics = forms.BooleanField(required=False)
	music = forms.BooleanField(required=False)
	beauty = forms.BooleanField(required=False)
	crafts = forms.BooleanField(required=False)
	technology = forms.BooleanField(required=False)
	fashion = forms.BooleanField(required=False)
	business = forms.BooleanField(required=False)

# class EditUserForm(ModelForm):
# 	class Meta:
			
# 		model = User
# 		fields = ['first_name', 'last_name', 'username','email']

class EditProfileForm(forms.Form):
	bio = forms.CharField(widget=forms.Textarea)
	location = forms.CharField()

class EditSubSectionsForm(forms.Form):
	sport_title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '  Add Sub Section... To add multiple sepereate with ":" (i.e. sub1:sub2:sub3)', 'style': 'width: 91%;'}),required=False, initial='')
	film_title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '  Add Sub Section... To add multiple sepereate with ":" (i.e. sub1:sub2:sub3)', 'style': 'width: 91%;'}),required=False,initial='')
	health_title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '  Add Sub Section... To add multiple sepereate with ":" (i.e. sub1:sub2:sub3)', 'style': 'width: 91%;'}),required=False,initial='')
	finance_title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '  Add Sub Section... To add multiple sepereate with ":" (i.e. sub1:sub2:sub3)', 'style': 'width: 91%;'}),required=False,initial='')
	auto_title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '  Add Sub Section... To add multiple sepereate with ":" (i.e. sub1:sub2:sub3)', 'style': 'width: 91%;'}),required=False,initial='')
	entrepreneurship_title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '  Add Sub Section... To add multiple sepereate with ":" (i.e. sub1:sub2:sub3)', 'style': 'width: 91%;'}),required=False,initial='')
	books_title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '  Add Sub Section... To add multiple sepereate with ":" (i.e. sub1:sub2:sub3)', 'style': 'width: 91%;'}),required=False,initial='')
	politics_title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '  Add Sub Section... To add multiple sepereate with ":" (i.e. sub1:sub2:sub3)', 'style': 'width: 91%;'}),required=False,initial='')
	music_title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '  Add Sub Section... To add multiple sepereate with ":" (i.e. sub1:sub2:sub3)', 'style': 'width: 91%;'}),required=False,initial='')
	beauty_title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '  Add Sub Section... To add multiple sepereate with ":" (i.e. sub1:sub2:sub3)', 'style': 'width: 91%;'}),required=False,initial='')
	crafts_title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '  Add Sub Section... To add multiple sepereate with ":" (i.e. sub1:sub2:sub3)', 'style': 'width: 91%;'}),required=False,initial='')
	technology_title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '  Add Sub Section... To add multiple sepereate with ":" (i.e. sub1:sub2:sub3)', 'style': 'width: 91%;'}),required=False,initial='')
	fashion_title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '  Add Sub Section... To add multiple sepereate with ":" (i.e. sub1:sub2:sub3)', 'style': 'width: 91%;'}),required=False,initial='')
	business_title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '  Add Sub Section... To add multiple sepereate with ":" (i.e. sub1:sub2:sub3)', 'style': 'width: 91%;'}),required=False,initial='')

class AddTool(forms.Form):
	tool_name = forms.CharField(max_length=155, widget=forms.TextInput(attrs={'placeholder': '  Product Name', 'style': 'width: 250px; border: solid; border-color: black; border-radius: 5px; border-width: 1px;'}))
	tool_link = forms.URLField(required=False, widget=forms.TextInput(attrs={'placeholder': '  Link to Product/Product Site', 'style': 'width: 250px; border: solid; border-color: black; border-radius: 5px; border-width: 1px;'}))
	# tool_content = forms.CharField(required=False,widget=forms.Textarea(attrs={'placeholder': 'Add short content','style': 'width: 97.5%; border-radius: 5px; resize: none','col': '45','rows': '2'}))
class AddPost(forms.Form):
	post_title = forms.CharField(required=False,max_length=155, widget=forms.TextInput(attrs={'placeholder': '  Title (optional)', 'style': 'width: 100%; height: 25px; border: solid; border-color: black; border-radius: 5px; border-width: 1px;'}))
	post_content = forms.CharField(required=False,widget=forms.Textarea(attrs={'placeholder': '  Enter Your Post Content Here', 'style':'width: 100%; height: 75px; resize: none; border: solid; border-color: black; border-radius: 5px; border-width: 1px;'}))
	post_image = forms.ImageField(required=False,widget=forms.FileInput())
	post_video = forms.URLField(required=False,widget=forms.TextInput(attrs={'placeholder': '  Url...', 'style': 'width: 95%; height: 25px; border: solid; border-color: black; border-radius: 5px; border-width: 1px;'}))
	post_file = forms.FileField(required=False)

class SignUpForm(UserCreationForm):
	first_name = forms.CharField(max_length=30,required=True,help_text='Required')
	last_name = forms.CharField(max_length=30,required=True,help_text='Required')
	birth_date = forms.DateField(required=True,help_text='Required YYYY-MM-DD')
	email = forms.EmailField(max_length=200,required=True,help_text='Required valid email address')
	phoneNumber = forms.IntegerField(required=True,help_text='Required Phone Number')
	location = forms.CharField(max_length=30,required=False,help_text='Optional')

	class Meta:
		model = User
		fields = ('username','first_name','last_name','birth_date','email','phoneNumber','location','password1','password2')



