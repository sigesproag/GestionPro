#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'rvidal'

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from models import Usuario

class FormUsuario(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

    class Meta:
        model = Usuario
        fields = ('username','email', 'is_superuser','first_name', 'last_name', 'cedula','celular', 'direccion')



class FormUsuarioChange(ModelForm):

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
    class Meta:
        model = Usuario
        fields = ('email', 'is_superuser','first_name', 'last_name','celular', 'direccion')

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(ModelForm, self).save(commit=False)
        #user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class AdminPasswordChangeForm(forms.Form):
    """
    A form used to change the password of a user in the admin interface.
    """
    error_messages = {
        'password_mismatch': ("Las contraseñas no coinciden."),
        'password_incorrect': ("La contraseña actual es incorrecta"),
    }
    required_css_class = 'required'
    password3 = forms.CharField(
         label= ("Contraseña Actual"),
        widget=forms.PasswordInput,
    )
    password1 = forms.CharField(
        label= ("Nueva Contraseña"),
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label=("Confirmación Contraseña"),
        widget=forms.PasswordInput,
        help_text=("Indroduzca ésta contraseña para confirmar la anterior."),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(AdminPasswordChangeForm, self).__init__(*args, **kwargs)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        return password2

    def save(self, commit=True):
        """
        Saves the new password.
        """
        password3 = self.cleaned_data.get('password3')
        if self.user.check_password(password3):
            self.user.set_password(self.cleaned_data["password1"])
        else:
            raise forms.ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        if commit:
            self.user.save()
        return self.user

    def _get_changed_data(self):
        data = super(AdminPasswordChangeForm, self).changed_data
        for name in self.fields.keys():
            if name not in data:
                return []
        return ['password']
    changed_data = property(_get_changed_data)