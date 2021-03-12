import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from .models import BookInstance


class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")

    # clean and validate
    def clean_renewal_date(self):
        print('clean_renewal_date called')
        data = self.cleaned_data['renewal_date']

        today = datetime.date.today()
        print(data, today, data < datetime.date.today())
        # check if user enter new date older than today
        if data < datetime.date.today():
            print(f'under validation check {data<today}')
            raise ValidationError(_('Invalid date - renewal in past'), code='invalid')

        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            print(f'under validation check {data < today+datetime.timedelta(weeks=4)}')
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'), code='invalid')
        # return clean data
        return data


class RenewBookModelForm(forms.ModelForm):
    class Meta:
        model = BookInstance
        # fields = '__all__'
        fields = ['due_back']
        labels = {'due_back': _('Renewal Date')}
        help_texts = {'due_back': _('Enter a date between now and 4 weeks (default 3).')}

    def clean_due_back(self) -> object:
        data = self.cleaned_data['due_back']

        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))
        if data > datetime.date.today()+datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))
        return data
