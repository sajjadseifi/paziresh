from django.forms.widgets import ClearableFileInput
from pathlib import Path

class CustomImageInput(ClearableFileInput):
    template_name = "widgets/custom_image_input.html"
