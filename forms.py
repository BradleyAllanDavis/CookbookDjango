from django import forms
from django.forms.utils import ErrorList

from cookbook.models import FoodGroup, Tag, Nutrient


class CookbookForm(forms.Form):
    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=None,
                 empty_permitted=False, field_order=None,
                 use_required_attribute=None):
        super(CookbookForm, self).__init__(data, files, auto_id, prefix,
            initial, error_class, label_suffix, empty_permitted, field_order,
            use_required_attribute)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = "form-control"


class SimpleSearchForm(CookbookForm):
    recipe_name_search_term = forms.CharField(label="Search", max_length=100)


class AdvancedSearchForm(CookbookForm):
    recipe_name_search_term = forms.CharField(max_length=100, required=False,
        label='Recipe name contains')
    ingredient_name_search_term = forms.CharField(
        label="and ingredient names contain", max_length=100, required=False)
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(),
        required=False, label="and tags contains all of")
    food_groups = forms.ModelMultipleChoiceField(
        queryset=FoodGroup.objects.all(), required=False,
        label="and food groups contain all of")


class SaveSearchForm(CookbookForm):
    saved_search_name = forms.CharField(max_length=100, required=True,
        label="Name for saved search")


class NutritionPreferenceForm(CookbookForm):
    nutrients = forms.ModelMultipleChoiceField(
        queryset=Nutrient.objects.exclude(
            id__in=[208, 204, 606, 605, 601, 307, 205, 291, 269, 203]),
        required=True)

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=None,
                 empty_permitted=False, field_order=None,
                 use_required_attribute=None):
        super(NutritionPreferenceForm, self).__init__(data, files, auto_id,
            prefix, initial, error_class, label_suffix, empty_permitted,
            field_order, use_required_attribute)
        self.fields['nutrients'].widget.attrs['size'] = '20'


class CreateUserForm(CookbookForm):
    username = forms.CharField(max_length=100, required=True)
    email = forms.CharField(max_length=100, required=False)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)


class SortRecipeIngredientsByNutrientForm(CookbookForm):
    nutrient = forms.ModelChoiceField(queryset=Nutrient.objects.all(),
        required=True)
