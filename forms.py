from django import forms

class SimpleSearchForm(forms.Form):
	search_term = forms.CharField(label="Search", max_length=100)


class AdvancedSearchForm(forms.Form):
	recipe_name_search_term = forms.CharField(label="Search", max_length=100)
	tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all())
	foodgroups = forms.ModelMultipleChoiceField(queryset=FoodGroup.objects.all())
	ingredient_name_search_term = forms.CharField(label="Search", max_length=100)		
