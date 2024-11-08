from django.contrib import admin
from ..models import QuizSession, Quiz
from ..forms import AddQuizzesForm

class QuizInline(admin.StackedInline): 
    model = Quiz
    fields = ['title']
    extra = 1
    



@admin.register(QuizSession)
class QuizSessionAdmin(admin.ModelAdmin):
    '''Admin View for QuizSession'''
    form = AddQuizzesForm
    list_display = ('date', 'duration', 'status')
    # list_filter = ('',)
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        selected_quizzes = form.cleaned_data.get('quizzes')
        if selected_quizzes:
            for quiz in selected_quizzes:
                quiz.quiz_session = obj 
                quiz.save()
