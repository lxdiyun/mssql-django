from django import forms


class BookQueryForm(forms.Form):
    book_ssid_list = forms.CharField(widget=forms.Textarea)

    def get_ssid_list(self):
        raw_list_string = self.cleaned_data['book_ssid_list']

        return raw_list_string.split()
