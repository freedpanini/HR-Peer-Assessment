from django.shortcuts import render, redirect, get_object_or_404
from .models import PeerAssessment, Question, Answer, Submission
from .forms import PeerAssessmentForm, QuestionForm, OptionForm

# Create your views here.
def create_assessment(request):
    if request.method == "POST":
        form = PeerAssessmentForm(request.POST)
        if form.is_valid():
            peer_assessment = form.save(commit=False)
            peer_assessment.creator = request.user
            peer_assessment.save()
            return redirect("", pk=peer_assessment.id)
    else:
        form = PeerAssessmentForm()

    return render(request, "create_assessment.html", {"form": form})

def delete_assessment(request, pk):
    peer_assessment = get_object_or_404(PeerAssessment, pk=pk, creator=request.user)
    if request.method == "POST":
        peer_assessment.delete()

    return redirect("")

def create_question(request, pk):
    peer_assessment = get_object_or_404(PeerAssessment, pk=pk, creator=request.user)
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.peer_assessment = peer_assessment
            question.save()
            return redirect("", peer_assessment_pk=pk, question_pk=question.pk)
    else:
        form = QuestionForm()

    return render(request, "create_question.html", {"peer_assessment": peer_assessment, "form": form})

def create_option(request, peer_assessment_pk, question_pk):

    peer_assessment = get_object_or_404(PeerAssessment, pk=peer_assessment_pk, creator=request.user)
    question = Question.objects.get(pk=question_pk)
    if request.method == "POST":
        form = OptionForm(request.POST)
        if form.is_valid():
            option = form.save(commit=False)
            option.question_id = question_pk
            option.save()
    else:
        form = OptionForm()

    options = question.option_set.all()
    return render(request, "peer_assessment/options.html", {
        "peer_assessment": peer_assessment, "question": question, "options": options, "form": form
        },
    )