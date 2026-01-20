from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Post

# Formulário de Cadastro Inicial
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full bg-transparent border border-gray-300 dark:border-gray-600 p-4 rounded-xl outline-none focus:ring-2 focus:ring-blue-500 dark:text-white transition-all placeholder-gray-500'
            })

# Formulário de Edição de Perfil
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'profile_pic', 'cover_image', 'bio']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-700 p-3 rounded-lg focus:ring-2 focus:ring-blue-400 outline-none text-black dark:text-white transition'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'w-full bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-700 p-3 rounded-lg focus:ring-2 focus:ring-blue-400 outline-none text-black dark:text-white transition',
                'rows': '3'
            }),
            'profile_pic': forms.FileInput(attrs={
                'class': 'block w-full text-sm text-gray-500 dark:text-gray-400 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 dark:file:bg-blue-900/30 file:text-blue-700 dark:file:text-blue-400 hover:file:bg-blue-100 dark:hover:file:bg-blue-900/50'
            }),
            'cover_image': forms.FileInput(attrs={
                'class': 'block w-full text-sm text-gray-500 dark:text-gray-400 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 dark:file:bg-blue-900/30 file:text-blue-700 dark:file:text-blue-400 hover:file:bg-blue-100 dark:hover:file:bg-blue-900/50'
            }),
        }

# Formulário de Postagem
class PostForm(forms.ModelForm): 
    class Meta:
        model = Post
        fields = ['content', 'image', 'video'] 
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'w-full bg-transparent border-none focus:ring-0 text-xl outline-none resize-none text-black dark:text-white placeholder-gray-500',
                'placeholder': 'O que está acontecendo?',
                'rows': '3'
            }),
        }