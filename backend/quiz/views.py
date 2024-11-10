from django.shortcuts import render
from django.views.generic import ListView, UpdateView
from django.views import View
from django.shortcuts import get_object_or_404, redirect
from .models import Quiz, Question
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import QuizForm, QuestionOptionFormSet, QuestionForm
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
        ic(questions)
    return render(
        request,
        "quiz/teacher/update.html",
        {
            "form": form,
            "questions": questions,
            "quiz_id": ic(quiz.id)},
    )


def create_question(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)

    if request.method == "POST":
        form = QuestionForm(request.POST)
        formset = QuestionOptionFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz  # Link question to quiz
            question.save()
            formset.instance = question
            formset.save()
            return render(
                request, "partials/success_message.html"
            )  # Partial template for successful save

        return render(
            request,
            "partials/question_form.html",
            {"form": form, "formset": formset, "quiz": quiz},
        )  # Return form with errors if invalid

    # GET request: show empty form
    form = QuestionForm()
    formset = QuestionOptionFormSet()
    return render(
        request,
        "partials/question_form.html",
        {
            "form": form,
            "formset": formset,
            "quiz": quiz},
    )
