from django.shortcuts import render
from django.views.generic import ListView, UpdateView
from django.views import View
from django.shortcuts import get_object_or_404, redirect
from .models import Quiz, Question, QuestionOption
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import QuizForm, QuestionOptionFormSet, QuestionForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from icecream import ic


class TeacherUserMixin:
    def get_teacher(self):
        user = self.request.user
        return user.teacher if hasattr(user, "teacher") and user.is_teacher else None


class QuizTeacherMixin(TeacherUserMixin):
    model = Quiz

    def get_queryset(self):
        teacher = self.get_teacher()

        if teacher:
            queryset = super().get_queryset()
            return queryset.get_quizzes_for_teacher(teacher.id)

        return self.model.objects.none()


class QuizTeacherUpdateView(View, QuizTeacherMixin):
    def get(self, request, quiz_id, *args, **kwargs):
        quizzes = Quiz.objects.filter(id=quiz_id)
        if quizzes.exists():
            quiz = quizzes.first()

        return render(request, "quiz/teacher/list.html", {"quizzes": quizzes})


class QuizTeacherListView(LoginRequiredMixin, QuizTeacherMixin, ListView):
    model = Quiz
    template_name = "quiz/teacher/list.html"
    context_object_name = "quizzes"


class QuizTeacherUpdateView(LoginRequiredMixin, QuizTeacherMixin, ListView, UpdateView):
    model = Quiz
    template_name = "quiz/teacher/update.html"
    success_url = reverse_lazy("quiz:teacher_quiz_list")
    fields = [
        "title",
        "number_of_questions",
        "easy_questions_count",
        "medium_questions_count",
        "hard_questions_count",
        "is_randomized",
    ]


def quiz_teacher_update_view(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    form = QuizForm()
    if request.method == "POST":
        form = QuizForm(request.POST, instance=quiz)
        if form.is_valid():
            form.save()
            return redirect("quiz:teacher_quiz_list")
    else:
        form = QuizForm(instance=quiz)
        questions = quiz.quiz_questions.all()
    return render(
        request,
        "quiz/teacher/update.html",
        {"form": form, "questions": questions, "quiz_id": ic(quiz.id)},
    )


def create_question(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    correct_option_selected = False  # Track if at least one option is marked as correct

    if request.method == "POST":
        form = QuestionForm(request.POST)
        formset = QuestionOptionFormSet(
            request.POST, queryset=QuestionOption.objects.none()
        )

        if form.is_valid() and formset.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()

            # Save formset and handle "is_correct" selection
            for option_form in formset:
                option = option_form.save(commit=False)
                option.question = question
                # Check if the current option's prefix matches the selected "is_correct" value
                if ic(request.POST.get("is_correct")) == option_form.prefix:
                    option.is_correct = True
                    correct_option_selected = True  # Track if at least one option is marked as correct
                else:
                    option.is_correct = False
                option.save()
                
        # Check if at least one option is marked as correct
        if not correct_option_selected:
            formset.non_form_errors = ["Please select at least one correct option."]
            return render(
                request, "partials/question_form.html", {"form": form, "formset": formset, 'quiz_id':quiz_id}
            )
        return render(request, "partials/success_message.html", {'quiz_id':quiz_id})

    # For GET request, return the empty form and formset
    form = QuestionForm()
    formset = QuestionOptionFormSet()
    return render(
        request,
        "partials/question_form.html",
        {"form": form, "formset": formset, "quiz_id": quiz_id},
    )

def question_list(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    questions = quiz.quiz_questions.all()
    
    page_number = request.GET.get('page', 1)
    
    # Set the number of questions per page
    questions_per_page = 10
    paginator = Paginator(questions, questions_per_page)
    page_obj = paginator.get_page(page_number)
    
    if request.htmx:
        return render(request, 'partials/question_list.html', {'page_obj': page_obj, 'quiz_id':quiz_id})
    