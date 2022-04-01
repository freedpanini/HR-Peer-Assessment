from django.shortcuts import render, redirect
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
