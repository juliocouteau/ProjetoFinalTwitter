from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Post, Comment

# Isso faz com que o seu Usuário customizado apareça corretamente
admin.site.register(User, UserAdmin)

# Isso faz com que as Postagens apareçam no painel
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'content', 'created_at') # Colunas que vão aparecer na lista
    search_fields = ('content', 'author__username')   # Barra de busca

# Isso faz com que os Comentários apareçam no painel
admin.site.register(Comment)