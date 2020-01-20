from django import forms
from .models import AddEmailHooksModel, EmailTemplateModel, MainEmailLayoutModel


class AddEmailHookForm(forms.Form):
    title = forms.CharField(required=True)
    hook = forms.CharField(required=True)
    description = forms.CharField(widget=forms.Textarea,required=True)
    status = forms.CharField(required=True)

    class Meta:
        model = AddEmailHooksModel
        fields = ('title','hook','description','status')

    def clean(self):
        cleaned_data = super(AddEmailHookForm, self).clean()
        return cleaned_data


class EmailTemplateForm(forms.Form):
    emailhooks = forms.CharField(required=True)
    subject = forms.CharField(required=True)
    ckeditor = forms.CharField(widget=forms.Textarea,required=True)
    footer_text = forms.CharField(required=True)
    email_preference = forms.CharField(required=True)
    status = forms.CharField(required=True)

    class Meta:
        model = EmailTemplateModel
        fields = ('emailhooks', 'subject', 'ckeditor', 'footer_text','email_preference','status')

    def clean(self):
        cleaned_data = super(EmailTemplateForm, self).clean()
        return cleaned_data


class AddMainEmailLayoutForm(forms.Form):
    title = forms.CharField(required=True)
    layout_html = forms.CharField(widget=forms.Textarea,required=True)

    class Meta:
        model = MainEmailLayoutModel
        fields = ('title','layout_html')

    def clean(self):
        cleaned_data = super(AddMainEmailLayoutForm, self).clean()
        return cleaned_data