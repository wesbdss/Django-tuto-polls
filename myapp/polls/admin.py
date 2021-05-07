from django.contrib import admin

# Register your models here.

from .models import Question, Choice
# muito pesado
# class ChoiceInline(admin.StackedInline):
#     model = Choice
#     extra = 0

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 0
class QuestionAdmin(admin.ModelAdmin):
    # option 1
    # fields = ['pub_date', 'question_text']

    # option 2
    fieldsets = [
        ("Questions Data", {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date']})
    ]

    # Inlines
    inlines = [ChoiceInline]

    # list_Display
    list_display = ('question_text', 'pub_date', 'was_published_recently')

    # Filter a direita
    list_filter =['pub_date']

    # Pesquisa
    search_fields = ['question_text']





admin.site.register(Question, QuestionAdmin)
# admin.site.register(Choice)