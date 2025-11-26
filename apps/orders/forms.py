from django import forms

# --------------------------------------------------------
# Checkout form
# --------------------------------------------------------
class CheckoutForm(forms.Form):
    """
    Form for collecting delivery information during checkout.
    Fields include optional address and postal code.
    """
    address = forms.CharField(
        label="آدرس تحویل",  # Delivery address
        required=False,
        widget=forms.Textarea(attrs={'rows': 2})  # Display as a small textarea
    )
    postal_code = forms.CharField(
        label="کد پستی",  # Postal/ZIP code
        required=False
    )