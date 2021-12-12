from django import forms

class EmailPostForm(forms.Form):
    nombre = forms.CharField(max_length=25)
    apellido = forms.CharField(max_length=25)
    email = forms.EmailField()
    para = forms.EmailField()
    comentarios = forms.CharField(required=False, widget=forms.Textarea)

class EmailBlogForm(forms.Form):
    nombre = forms.CharField(max_length=25)
    apellido = forms.CharField(max_length=25)
    email = forms.EmailField()
    
    comentarios = forms.CharField(required=False, widget=forms.Textarea)