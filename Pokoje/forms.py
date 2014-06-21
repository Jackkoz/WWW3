from django import forms
from Pokoje.models import Reservation, Attribute


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ('date', 'begin', 'end')


class SearchForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields['min_capacity'].required = False
        self.fields['max_capacity'].required = False
        self.fields['key'].required = False
        self.fields['attributes'].required = False
        self.fields['attributes'].choices = [(x,x) for x in Attribute.objects.all()]

    key = forms.CharField(max_length=50)
    min_capacity = forms.IntegerField()
    max_capacity = forms.IntegerField()
    attributes = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)
