from django import forms
from .models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Post
class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'picture']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save Changes'))
        

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['body', 'picture']
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Say Something, Anything...'}),
            'picture': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }