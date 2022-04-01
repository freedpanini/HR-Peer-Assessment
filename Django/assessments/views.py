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

    return render(request, "create_question.html", {"survey": peer_assessment, "form": form})
