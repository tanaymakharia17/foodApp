from django import forms

from menu.models import Category, FoodItem

class CategoryForm(forms.ModelForm):
    
    class Meta:
        model = Category
        fields = ['category_name', 'description']

    
    def clean(self):
        cleaned_data = super(CategoryForm, self).clean()
        cleaned_data['category_name'] = cleaned_data['category_name'].capitalize()
