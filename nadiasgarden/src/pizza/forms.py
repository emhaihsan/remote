from django import forms
from .models import Pizza
from .models import Size

# class PizzaForm(forms.Form):
#     topping1 = forms.CharField(label='Topping 1', max_length=100, widget=forms.PasswordInput)
#     topping2 = forms.CharField(label='Topping 2', max_length=100)
#     size = forms.ChoiceField(label='Size', choices=[('Small', 'S'), ('Medium', 'M'), ('Large', 'L')])

class PizzaForm(forms.ModelForm):
    # email = forms.EmailField()
    # url = forms.URLField()
    class Meta:
        model = Pizza
        fields = ['topping1', 'topping2', 'size']
        labels = {'topping1': 'Topping 1', 
                  'topping2': 'Topping 2'}

class MultiplePizzaForm(forms.Form):
    number = forms.IntegerField(min_value=1, max_value=6)