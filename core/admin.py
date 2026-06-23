# core/admin.py

from django.contrib import admin
from .models import Profile, Experience, Skill, Project, ContactMessage


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display  = ('full_name', 'tagline', 'email')


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display  = ('role', 'company', 'start_date', 'end_date', 'is_current')
    list_filter   = ('is_current',)
    search_fields = ('company', 'role')
    list_editable = ('is_current',)  # toggle "current job" right from the list


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display  = ('name', 'category', 'proficiency')
    list_filter   = ('category',)
    search_fields = ('name',)
    list_editable = ('proficiency',)  # adjust % without opening each record


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display  = ('title', 'tech_stack', 'live_link', 'created_at')
    search_fields = ('title', 'tech_stack')
    list_filter   = ('created_at',)
    readonly_fields = ('created_at',)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display  = ('name', 'email', 'subject', 'sent_at', 'is_read')
    list_filter   = ('is_read', 'sent_at')
    search_fields = ('name', 'email', 'subject')
    list_editable = ('is_read',)   # mark as read directly from the list
    readonly_fields = ('name', 'email', 'subject', 'message', 'sent_at')