from django import forms
from autoslug import AutoSlugField

from .models import Category, Product, Order

class CategoriesForm(forms.ModelForm):
    name = forms.CharField(required=True)
    
    def clean(self):
        cleaned_data = super(CategoriesForm, self).clean()
        name = cleaned_data.get('name')
    
    class Meta:
        model = Category
        fields = ('name',)

class ProductsForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    name = forms.CharField()
    slug = AutoSlugField(unique=True, always_update=False, populate_from="name")
    image = forms.ImageField(required=False)
    description = forms.CharField(widget=forms.Textarea)
    price = forms.DecimalField()
    is_available = forms.IntegerField()
    
    def clean(self):
        cleaned_data = super(ProductsForm, self).clean()
        category = cleaned_data.get('category')
        name = cleaned_data.get('name')
        image = cleaned_data.get('image')
        description = cleaned_data.get('description')
        price = cleaned_data.get('price')
        is_available = cleaned_data.get('is_available')
        
    
    class Meta:
        model = Product
        fields = ('category', 'name', 'image', 'description', 'price', 'is_available',)
        
class OrdersForm(forms.ModelForm):
    specific_product = forms.ModelChoiceField(queryset=Product.objects.all())
    quantity = forms.IntegerField(required=True)
    price = forms.DecimalField(required=True)
    name = forms.CharField(required=True)
    cpf = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    address = forms.CharField(required=True)
    
    def clean(self):
        cleaned_data = super(OrdersForm, self).clean()
        specific_product = cleaned_data.get('specific_product')
        quantity = cleaned_data.get('quantity')
        price = cleaned_data.get('price')
        name = cleaned_data.get('name')
        cpf = cleaned_data.get('cpf')
        email = cleaned_data.get('email')
        address = cleaned_data.get('address')
        
    
    class Meta:
        model = Order
        fields = ('specific_product', 'quantity', 'price', 'name', 'cpf', 'email', 'address',)