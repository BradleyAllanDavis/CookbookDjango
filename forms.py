from django import forms

from cookbook.models import FoodGroup, Tag


class SimpleSearchForm(forms.Form):
	search_term = forms.CharField(label="Search", max_length=100)


class AdvancedSearchForm(forms.Form):
	recipe_name_search_term = forms.CharField(max_length=100, required=False,
		label='Recipe name should contain')
	tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(),
		required=False)
	food_groups = forms.ModelMultipleChoiceField(
		queryset=FoodGroup.objects.all(), required=False)
	ingredient_name_search_term = forms.CharField(
		label="Ingredients should contain", max_length=100, required=False)
