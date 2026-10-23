from django import forms

from core.models import User


class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "profile_picture"]

        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "class": (
                        "input input-bordered w-full rounded-xl "
                        "bg-base-100 transition-colors "
                        "focus:input-primary"
                    ),
                    "placeholder": "Enter your first name",
                    "autocomplete": "given-name",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": (
                        "input input-bordered w-full rounded-xl "
                        "bg-base-100 transition-colors "
                        "focus:input-primary"
                    ),
                    "placeholder": "Enter your last name",
                    "autocomplete": "family-name",
                }
            ),
            "profile_picture": forms.ClearableFileInput(
                attrs={
                    "class": (
                        "file-input file-input-bordered w-full "
                        "rounded-xl bg-base-100 "
                        "focus:file-input-primary"
                    ),
                    "accept": "image/*",
                    "aria-describedby": "profile-picture-help",
                }
            ),
        }

        help_texts = {
            "profile_picture": ("Choose an image to use as your profile picture."),
        }
