from ckeditor.widgets import CKEditorWidget
from django.contrib import admin
from django import forms
# Register your models here.
from questions.models import Question, Comment

class QuestionAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Question
        fields = '__all__'



class QuestionAdmin(admin.AdminSite):
    site_header = 'StackOverflow question administration'
    site_title = 'Question administration'
    index_title = 'Admin panel'


question_admin_site = QuestionAdmin(name='questionadmin')

class CommentAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Comment
        fields = '__all__'

class CommentInline(admin.StackedInline):
    form = CommentAdminForm
    model = Comment
    fields = ('user', 'description')
    extra = 1

@admin.register(Question, site=question_admin_site)
class QuestionAdmin(admin.ModelAdmin):
    form = QuestionAdminForm
    list_display = ('title', 'date_created', 'views', 'user')
    fieldsets = (
        ('Required information', {
            'description': 'This fields are required for each event.',
            'fields': ('title', 'description', ('views', 'user'))
        }),
    )
    # readonly_fields = ('title', 'user', 'views')
    ordering = ('date_created', 'title')
    search_fields = ('title', 'user')
    inlines = [
        CommentInline
    ]


# class QuestionInline(admin.TabularInline):
#     model = Question
#     fields = ('title', 'user', 'date_created', 'description')

def set_is_useful(modeladmin, request, queryset):
    queryset.update(is_useful=True)

set_is_useful.short_description = 'Set comments useful'

@admin.register(Comment, site=question_admin_site)
class CommentAdmin(admin.ModelAdmin):
    form = CommentAdminForm
    list_display = ('user', 'question', 'date_created', 'like')
    # readonly_fields = ('user', 'question')
    ordering = ('date_created', 'question')
    search_fields = ('question', 'user')
    list_filter = (
        'like',
        'is_useful',
    )
    fieldsets = (
        ('Comment information', {
            'description': 'This fields are required for each event.',
            'fields': ('description', ('question', 'user', 'is_useful'))
        }),
    )
    actions = [
        set_is_useful,
    ]
    # inlines = [
    #     QuestionInline
    # ]


