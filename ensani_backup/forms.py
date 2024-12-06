from django import forms

class BackupUploadForm(forms.Form):
    backup_file = forms.FileField()
