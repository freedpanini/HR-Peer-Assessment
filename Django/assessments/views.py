#<<<<<<< HEAD

# Create your views here.

#=======
from django.shortcuts import render, redirect, get_object_or_404
from .models import PeerAssessment, Question, Answer, Submission
from .forms import PeerAssessmentForm, QuestionForm, OptionForm, FreeResponseForm
from django.contrib.auth.decorators import login_required
from django.http import Http404
from courses.models import Course, Registration, Invitation, Team
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse



# Create your views here.
@login_required
def create_assessment(request):
    if request.method == "POST":
        form = PeerAssessmentForm(request.POST)
        if form.is_valid():
            peer_assessment = form.save(commit=False)
            peer_assessment.creator = request.user
            peer_assessment.course_id = 1
            peer_assessment.save()
            return redirect("edit_assessment", pk=peer_assessment.id)
    else:
        form = PeerAssessmentForm()

    return render(request, "assessments/create_assessment.html", {"form": form})

@login_required
def edit_assessment(request, pk):
    try:
        peer_assessment = PeerAssessment.objects.prefetch_related("question_set__option_set").get(
            pk=pk, creator=request.user, is_active=False
        )
    except PeerAssessment.DoesNotExist:
        print("Doesnt exist")
        raise Http404()

    try:
        peer_assessment2 = PeerAssessment.objects.prefetch_related("freeresponse_set").get(
            pk=pk, creator=request.user, is_active=False
        )
    except PeerAssessment.DoesNotExist:
        raise Http404()

    if request.method == "POST":
        peer_assessment.is_active = True
        peer_assessment.save()
        course = Course.objects.get(course_id=peer_assessment.course_id)
        registrations = Registration.objects.filter(course_id=course.course_id)
        student_emails = [o.student for o in registrations]

        host = request.get_host()
        public_path = reverse("assessment-start", args=[pk])
        url = f"{request.scheme}://{host}{public_path}"

        send_mail(f'Peer Assessment Created! Go to link to fill it out! ',
	    url,
	    settings.EMAIL_HOST_USER,
	    student_emails,
	    fail_silently=False,html_message=url)

        return redirect("home")
    else:
        questions = peer_assessment.question_set.all()
        frees = peer_assessment2.freeresponse_set.all()
        return render(request, "assessments/edit_assessment.html", {"peer_assessment": peer_assessment, "questions": questions, "frees":frees})

@login_required
def delete_assessment(request, pk):
    peer_assessment = get_object_or_404(PeerAssessment, pk=pk, creator=request.user)
    if request.method == "POST":
        peer_assessment.delete()

    return redirect("")

@login_required
def create_question(request, pk):
    peer_assessment = get_object_or_404(PeerAssessment, pk=pk)#, creator=request.user)
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.peer_assessment = peer_assessment
            question.save()
            return redirect("create_options", peer_assessment_pk=pk, question_pk=question.pk)
    else:
        form = QuestionForm()

    return render(request, "assessments/create_question.html", {"peer_assessment": peer_assessment, "form": form})

@login_required
def create_options(request, peer_assessment_pk, question_pk):

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
    return render(request, "assessments/create_options.html", {
        "peer_assessment": peer_assessment, "question": question, "options": options, "form": form
        },
    )

@login_required
def create_free_response(request, peer_assessment_pk):
    peer_assessment = get_object_or_404(PeerAssessment, pk=peer_assessment_pk, creator=request.user)
    if request.method == 'POST':
        form = FreeResponseForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.peer_assessment = peer_assessment
            question.save()
            print("valid form saved")
            return redirect("edit_assessment", pk=peer_assessment.pk)

    else: 
        form = FreeResponseForm()
        print("INVALID")
    return render(request, "assessments/create_free_response.html", {
        "peer_assessment": peer_assessment,  "form": form } #, "question": question, "options": response, "form": form},
    )        

@login_required
def assessments_list(request):
    peer_assessments = PeerAssessment.objects.filter(creator=request.user).order_by("-creation_date").all()
    return render(request, "assessments/assessments_list.html", {"peer_assessments": peer_assessments})

