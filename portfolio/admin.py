from django.contrib import admin
from .models import Portfolio, Skill, Socials, Message

class SkillInline(admin.StackedInline):
    model = Skill
    extra = 1


class SocialsInline(admin.StackedInline):
    model = Socials
    extra = 1


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    inlines = [
        SkillInline,
        SocialsInline,
    ]


admin.site.register(Skill)
admin.site.register(Socials)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'email'
    )
