from django import forms

class SearchForm(forms.Form):
    title = forms.CharField(label='Szukana fraza', max_length=512, required=False)
    exact = forms.BooleanField(label='Dokładne wyszukiwanie', required=False)