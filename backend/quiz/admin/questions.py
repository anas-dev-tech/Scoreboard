from django.contrib import admin
from ..models import Quiz, Question, QuestionOption
from ..forms import QuestionOptionFormTabularInline, QuestionOptionInlineFormSet
from django.core.exceptions import ValidationError
from icecream import ic

class QuestionOptionInline(admin.TabularInline):
    model = QuestionOption
    form = QuestionOptionFormTabularInline
    formset = QuestionOptionInlineFormSet
    min_num = 2
    max_num = 4
    extra = 4

    class Media:
        js = ('js/admin/radio_single_selection.js',)  # Custom JS for enforcing single radio selection
        
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [QuestionOptionInline]
    list_filter = ['quiz']
    exclude = ['answer']


    def save_related(self, request, form, formsets, change):
        # Custom logic before saving the related QuestionOption instances
        super().save_related(request, form, formsets, change)
        number_of_answers = 0
        for formset in formsets:
            if formset.model == QuestionOption:
                for form in formset.forms:
                    is_answer = form.cleaned_data['is_answer']
                    if is_answer:
                        number_of_answers += 1
                        correct_answer = form.instance
        if number_of_answers != 1:
            raise ValidationError("A question must have exactly one answer.")
                                    
        # Perform your custom logic here
        if correct_answer:
            question = form.instance.question.answer = correct_answer
            question.save()
        
