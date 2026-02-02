from django import forms
from import_export.forms import ImportForm, ConfirmImportForm

from commons.models import University
from indicators.models import Indicator


class SubjectDataImportForm(ImportForm):
    indicator = forms.ModelChoiceField(queryset=Indicator.objects.all(), required=True)
    university = forms.ModelChoiceField(
        queryset=University.objects.all(), required=True
    )


class SubjectDataConfirmImportForm(ConfirmImportForm):
    indicator = forms.ModelChoiceField(queryset=Indicator.objects.all(), required=True)
    university = forms.ModelChoiceField(
        queryset=University.objects.all(), required=True
    )
