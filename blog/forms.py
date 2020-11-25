from django import forms
from .models import Subscription

class ContactForm(forms.Form):
    Your_email = forms.EmailField(widget=forms.TextInput(attrs={'class' : 'contact_form'}), required=True)
    subject = forms.CharField(widget=forms.TextInput(attrs={'class' : 'contact_form'}), required=True)
    message = forms.CharField(widget=forms.Textarea(attrs={'class' : 'contact_form_text'}), required=True)

class SubscriptionForm(forms.ModelForm):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'contact_form'

    class Meta:
        model = Subscription
        fields = ('first_name', 'e_mail',)