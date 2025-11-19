from django import forms


class CheckoutForm(forms.Form):
    address = forms.CharField(label="آدرس تحویل", required=False, widget=forms.Textarea(attrs={'rows':2}))
    postal_code = forms.CharField(label="کد پستی", required=False)