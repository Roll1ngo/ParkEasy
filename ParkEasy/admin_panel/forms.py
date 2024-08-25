from django import forms
from parkings.models import UserProfile, Plates, Rates
from django.forms import modelformset_factory
from django.forms import inlineformset_factory


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'phone_number', 'email']


class PlatesForm(forms.ModelForm):
    class Meta:
        model = Plates
        fields = ['plate_number', 'is_banned', 'id']
        widgets = {
            'plate_number': forms.TextInput(attrs={'maxlength': '20'}),
            'is_banned': forms.CheckboxInput(),
        }


PlateFormSet = inlineformset_factory(
    UserProfile, Plates,
    form=PlatesForm,
    fields=('plate_number', 'is_banned', 'id'),
    extra=0, can_delete=True
)


class PlatesFormUser(forms.ModelForm):
    class Meta:
        model = Plates
        fields = ['plate_number', 'is_banned', 'id']
        widgets = {
            'plate_number': forms.TextInput(attrs={'maxlength': '20'}),
            'is_banned': forms.CheckboxInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        plate_number = cleaned_data.get('plate_number')
        is_banned = cleaned_data.get('is_banned')

        if not plate_number and not self.instance.pk:
            raise forms.ValidationError({
                'plate_number': 'This field is required.'
            })

        # Можна додати додаткові перевірки, якщо потрібно
        return cleaned_data


PlateFormSetUser = inlineformset_factory(
    UserProfile, Plates,
    form=PlatesFormUser,
    fields=('plate_number', 'is_banned', 'id'),
    extra=0,
    can_delete=True
)


class RateForm(forms.ModelForm):
    class Meta:
        model = Rates
        fields = ['rate']