from django import forms

class SendOTPForm(forms.Form):
    phone = forms.CharField(label='شماره موبایل', max_length=15)

class VerifyOTPForm(forms.Form):
    phone = forms.CharField(widget=forms.HiddenInput())
    code = forms.CharField(label='کد تایید', max_length=6)

class SignupForm(forms.Form):
    phone = forms.CharField(widget=forms.HiddenInput())
    full_name = forms.CharField(label='نام و نام خانوادگی', required=False)
    role = forms.ChoiceField(label='نقش', choices=(('customer','خریدار'),('seller','فروشنده')))

class SigninForm(forms.Form):
    phone = forms.CharField(label='شماره موبایل', max_length=15)