from django.shortcuts import render
from django.views.generic import ListView, UpdateView
from django.views import View
from django.shortcuts import get_object_or_404, redirect
from .models import Quiz, Question, QuestionOption
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import QuizForm, QuestionOptionFormSet, QuestionForm, QuizForm
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
    if request.method == "POST":
        form = QuestionForm(request.POST)
        formset = QuestionOptionFormSet(
            request.POST, queryset=QuestionOption.objects.none()
        )

        if form.is_valid() and formset.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()
            formset.instance = question
            formset.save()

            return render(
                request, "partials/success_message.html", {"quiz_id": quiz_id}
            )

        return render(
            request,
            "partials/question_form.html",
            {"form": form, "formset": formset, "quiz_id": quiz_id},
        )

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
    page_number = request.GET.get("page", 1)

    # Set the number of questions per page
    questions_per_page = 10
    paginator = Paginator(questions, questions_per_page)
    page_obj = paginator.get_page(page_number)

    if request.htmx:
        return render(
            request,
            "partials/question_list.html",
            {"page_obj": page_obj, "quiz_id": quiz_id},
        )


def edit_question(request, quiz_id, question_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    question = get_object_or_404(Question, pk=question_id, quiz=quiz)

    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        formset = QuestionOptionFormSet(request.POST, instance=question)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()

            # Return a response for HTMX to confirm form saved and reload the modal content
            return render(
                request,
                "partials/question_form.html",
                {
                    "form": form,
                    "formset": formset,
                    "quiz_id": quiz_id,
                    "message": "Question updated successfully!",
                    "question_id": question_id,
                    "type": "edit",
                },
            )
        else:
            # Provide error feedback to user if form is not valid
            return render(
                request,
                "partials/question_form.html",
                {
                    "form": form,
                    "formset": formset,
                    "quiz_id": quiz_id,
                    "question_id": question_id,
                    "errors": form.errors or formset.non_form_errors(),
                    "type": "edit",
                },
            )
    else:
        form = QuestionForm(instance=question)
        formset = QuestionOptionFormSet(instance=question)

    return render(
        request,
        "partials/question_form.html",
        {
            "form": form,
            "formset": formset,
            "quiz_id": quiz_id,
            "question_id": question_id,
            "type": "edit",
        },
    )



def create_quiz(request):
    form = QuizForm()
    if request.method == "POST":
        form = QuizForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            
            return redirect("quiz:teacher_quiz_list")
    return render(request, "quiz/partials/quiz/create.html", {"form": form})
