from django import forms

class SearchForm(forms.Form):
	search_term = forms.CharField(label="Search", max_length=100)
