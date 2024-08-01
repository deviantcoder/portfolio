from django.contrib import admin
from .models import Portfolio, Skill, Socials, Message, Project


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    pass


admin.site.register(Skill)
admin.site.register(Socials)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'email'
    )


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'visible',
        'updated',
    )