from django import forms

class SearchForm(forms.Form):
    title = forms.CharField(label='Tytuł piosenki', max_length=512)