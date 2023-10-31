from django import forms

from .services import get_key_words


class UserForm(forms.Form):
    data = forms.CharField(widget=forms.Textarea, label_suffix=": ", label="Key words", help_text="Enter key phrases for parsing, each word on a new line.")

    def __init__(self, user):
        super(UserForm, self).__init__()
        self.user = user
        self.fields["data"].initial = self.get_key_words_for_view()

    def get_key_words_for_view(self):
        return "\r\n".join(get_key_words(self.user))
