from django import forms
from .models import Quiz, QuizSession, Question, QuestionOption
from core.constants import QuizStatus
from icecream import ic
from django.forms.models import inlineformset_factory
from django.forms import BaseInlineFormSet


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
    class Meta:
        model = Quiz
        fields = (
            "title",
            "number_of_questions",
            "quiz_for",
            "is_randomized",
            "easy_questions_count",
            "medium_questions_count",
            "hard_questions_count",
            "status",
        )


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["text", "score", "difficulty_level"]


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
