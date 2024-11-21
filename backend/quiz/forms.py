from django import forms
from .models import Quiz, QuizSession, Question, QuestionOption
from core.constants import QuizStatus
from icecream import ic
from django.forms.models import inlineformset_factory
from django.forms import BaseInlineFormSet
from academics.models import CourseAssignment
from django.utils.safestring import mark_safe


class ExistingQuizForm(forms.ModelForm):
    quiz = forms.ModelChoiceField(
        queryset=Quiz.objects.filter(status=QuizStatus.READY),
        label="Select Existing Quiz",
    )

    class Meta:
        model = Quiz
        fields = ["quiz"]


class AddQuizzesForm(forms.ModelForm):
    quizzes = forms.ModelMultipleChoiceField(
        queryset=Quiz.objects.all(), widget=forms.SelectMultiple
    )

    class Meta:
        model = QuizSession
        fields = [
            "excluded_students",
            "date",
            "duration",
            "password",
            "status",
            "quizzes",
        ]

    def __init__(self, *args, **kwargs):
        super(AddQuizzesForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["quizzes"].initial = self.instance.quizzes.all()


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = "__all__"


class QuestionOptionFormTabularInline(forms.ModelForm):
    is_answer = forms.BooleanField(
        widget=forms.RadioSelect(choices=[(True, "Correct")]), required=False
    )

    class Meta:
        model = QuestionOption
        fields = "__all__"


from django.forms.models import BaseInlineFormSet
from django.core.exceptions import ValidationError
from .models import QuestionOption


class QuestionOptionInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        number_of_answers = 0
        correct_answer = None
        counter = 0
        for form in self.forms:
            counter += 1
            if self.can_delete and self._should_delete_form(form):

                continue

            is_answer = form.cleaned_data.get("is_answer", False)
            if is_answer:
                number_of_answers += 1
                correct_answer = form.instance
        ic(counter)
        if number_of_answers != 1:
            raise ValidationError("A question must have exactly one answer.")

        question = self.instance
        num_options = len(self.forms)
        ic(self.forms)
        ic(num_options)

        if question.is_true_or_false_question() and num_options != 2:
            raise ValidationError("True/False questions must have exactly 2 options.")

        if question.is_multiple_choice_question() and num_options < 2:
            raise ValidationError(
                "Multiple Choice questions must have at least 2 options."
            )


class QuizForm(forms.ModelForm):
    # def __init__(self, *args, user=None,**kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.user = user
    #     # Optionally, you can set initial values or limit choices based on `user`
    #     if self.user:
    #         teacher_syllabi = CourseAssignment.objects.filter(teacher=self.user.teacher)

    #         # Step 2: Exclude syllabi that are already associated with other quizzes
    #         excluded_syllabi = CourseAssignment.objects.filter(quizzes__isnull=False).distinct()

    #         # Step 3: Initialize the available syllabi, excluding those in other quizzes
    #         available_syllabi = teacher_syllabi.exclude(id__in=excluded_syllabi)

    #         # Step 4: If in update mode, add existing values back to the queryset
    #         if self.instance.pk:
    #             # Get the syllabi already associated with this quiz
    #             current_quiz_syllabi = self.instance.courses.all()
                
    #             # Include these syllabi in the available queryset
    #             available_syllabi = available_syllabi | current_quiz_syllabi

    #         # Set the queryset for `courses` field
    #         self.fields['course_assignments'].queryset = available_syllabi
            
            
    # def clean_courses(self):
    #     selected_syllabi = self.cleaned_data.get('course_assignments')
        
    #     # Check each syllabus to enforce validation
    #     for syllabus in selected_syllabi:
    #         # Condition 1: Ensure syllabus belongs to the teacher
    #         if syllabus.teacher != self.user.teacher:
    #             raise ValidationError(f"The syllabus {syllabus} does not belong to the current teacher.")
            
    #         # Condition 2: Ensure syllabus is not already linked to another quiz (if in create mode)
    #         if not self.instance.pk and syllabus.quizzes.exists():
    #             raise ValidationError(f"The syllabus {syllabus} is already associated with another quiz.")

    #     return selected_syllabi
    class Meta:
        model = Quiz
        fields = (
            "title",
            "number_of_questions",
            "is_randomized",
            "status",
        )




class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["text", "score"]


class QuestionOptionForm(forms.ModelForm):
    is_correct = forms.ChoiceField(
        choices=[(True, "Correct"),(False, "Incorrect")],
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        required=False
    )
    class Meta:
        model = QuestionOption
        fields = ["text", "is_correct"]


class BaseQuestionOptionFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        correct_option_selected = False

        for form in self.forms:
            if not form.cleaned_data.get('DELETE', False):
                # Check if this option is marked as correct
                if form.cleaned_data.get("is_correct", False):
                    if correct_option_selected:
                        raise forms.ValidationError("Only one option can be marked as correct.")
                    correct_option_selected = True

        if not correct_option_selected:
            raise forms.ValidationError("Please select at least one correct option.")


QuestionOptionFormSet = forms.inlineformset_factory(
    Question,
    QuestionOption,
    formset=BaseQuestionOptionFormSet,
    fields=("text", "is_correct"),
    min_num=2,
    validate_min=2,
    max_num=4,
    extra=2,
)


class UploadFileAIForm(forms.Form):
    file = forms.FileField(
        help_text=mark_safe('''<br>
                            <small>
                                <span style="color: red;">*</span> Only PDF and PPTX files are supported.
                            </small>
                            ''')
    )
    question_number = forms.IntegerField(min_value=1, label="Number of Questions")
    
    
    def clean_file(self):
        file = self.cleaned_data.get('file', )
        
        if not file.name.endswith(('.pdf', 'pptx')):
            raise forms.ValidationError("Only PDF and PPTX files are supported in this app.")