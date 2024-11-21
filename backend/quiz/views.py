from django.shortcuts import render
from django.views.generic import ListView, UpdateView
from django.views import View
from django.shortcuts import get_object_or_404, redirect
from .models import Quiz, Question, QuestionOption
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import (
    QuizForm,
    QuestionOptionFormSet,
    QuestionForm,
    QuizForm,
    UploadFileAIForm,
)
from core.utils import ImportData
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from icecream import ic
import time
from rules.contrib.views import permission_required, objectgetter




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



def list_quiz(request):
    teacher = request.user.teacher
    quizzes = Quiz.objects.filter(course_assignments__teacher=teacher)

    if request.htmx:
        ic("it is htmx")
        return render(request, "quiz/partials/quiz/list.html", {"quizzes": quizzes})
    
    return render(request, "quiz/teacher/list.html", {"quizzes": quizzes})


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

def update_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    form = QuizForm(user=request.user)
    if request.method == "POST":
        form = QuizForm(request.POST, user=request.user, instance=quiz)
        if form.is_valid():
            form.save()
            return redirect("quiz:teacher_quiz_list")
    else:
        form = QuizForm(user=request.user, instance=quiz)
        context = {"form": form, "quiz_id": quiz_id}

    if request.htmx:
        return render(request, "quiz/partials/quiz/update.html", context)
    return render(
        request,
        "quiz/teacher/update.html",
        context,
    )

def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    quiz_form = QuizForm(instance=quiz)
    questions = quiz.quiz_questions.all()
    context = {"quiz": quiz, 'form':quiz_form, "questions": questions}
    return render(request, "quiz/teacher/detail.html", context)

def upload_file_ai(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

@login_required
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
            "quiz/partials/question/form.html",
            {"form": form, "formset": formset, "quiz_id": quiz_id},
        )

    # For GET request, return the empty form and formset
    form = QuestionForm()
    formset = QuestionOptionFormSet()
    return render(
        request,
        "quiz/partials/question/form.html",
        {"form": form, "formset": formset, "quiz_id": quiz_id},
    )


@login_required
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


@login_required
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
                "quiz/partials/question/form.html",
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
                "quiz/partials/question/form.html",
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
        "quiz/partials/question/form.html",
        {
            "form": form,
            "formset": formset,
            "quiz_id": quiz_id,
            "question_id": question_id,
            "type": "edit",
        },
    )


@login_required
def create_quiz(request):
    if request.method == "POST":
        form = QuizForm(request.POST, user=request.user)
        if form.is_valid():

            quiz = form.save()

            return render(request, "quiz/partials/quiz/success_message.html")
        else:

            return render(request, "quiz/partials/quiz/create.html", {"form": form})

    form = QuizForm(user=request.user)
    return render(request, "quiz/partials/quiz/create.html", {"form": form})

import google.generativeai as genai

import random

def generate_question():
    topics = ["Science", "History", "Geography", "Technology", "Sports"]
    topic = random.choice(topics)

    question = f"What is the capital of {topic}?"

    correct_answer = {
        "Science": "Discovery",
        "History": "Change",
        "Geography": "Location",
        "Technology": "Innovation",
        "Sports": "Competition"
    }[topic]

    incorrect_answers = [
        "Failure",
        "Stagnation",
        "Isolation",
        "Regression"
    ]
    random.shuffle(incorrect_answers)

    all_answers = [correct_answer] + incorrect_answers
    random.shuffle(all_answers)

    return question, all_answers


def create_question_AI(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    genai.configure(api_key="AIzaSyAWU8HmDsfMk96vMaio3nd4id2BwCVKbH4")
    model = genai.GenerativeModel('gemini-1.5-flash-latest')


    if request.method == "POST":
        form = UploadFileAIForm(request.POST, request.FILES)

        if form.is_valid():
            file = request.FILES.get('file', None)
            question_number = form.cleaned_data["question_number"]
        
            if file.name.endswith(".pdf"):
                text_data = ImportData(file).pdf_to_text()
            
            if file.name.endswith(".pptx"):
                text_data = ImportData(file).pptx_to_text()
                
            
            time.sleep(10)

            return render(request, 'quiz/partials/question/AI/receive.html', {"message":text_data})
        
        ic("not valid_form")
        
        return render(request, "quiz/partials/question/AI/submit.html", {"form": form, "quiz_id": quiz_id})
        
    else:
        form = UploadFileAIForm()
        return render(
            request,
            "quiz/partials/question/AI/submit.html",
            {"form": form, "quiz_id": quiz_id},
        )
