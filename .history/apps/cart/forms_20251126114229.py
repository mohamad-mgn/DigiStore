from django import forms

# --------------------------------------------------------
# Cart Update Form
# --------------------------------------------------------
class CartUpdateForm(forms.Form):
    """
    Form to update the quantity of a product in the cart.
    Ensures that quantity is at least 1.
    """
    quantity = forms.IntegerField(
        min_value=1,  # Minimum allowed quantity
        label="تعداد"  # Persian label for the form field
    )