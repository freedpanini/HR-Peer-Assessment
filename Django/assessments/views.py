
#<<<<<<< HEAD

# Create your views here.

#=======
from django.shortcuts import render, redirect, get_object_or_404
from .models import FreeResponseAnswer, PeerAssessment, Question, Answer, Submission
from courses.models import Course, Registration, Invitation, Team
from .forms import FreeResponseAnswerForm, PeerAssessmentForm, QuestionForm, OptionForm, FreeResponseForm, AnswerForm, BaseAnswerFormSet, SubmissionForm
from django.contrib.auth.decorators import login_required
from django.http import Http404
from courses.models import Course, Registration
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.forms.formsets import formset_factory
from django.db import transaction
from datetime import datetime
from django.utils import timezone

# Create your views here.
@login_required
def create_assessment(request, course_pk):
    if request.method == "POST":
        form = PeerAssessmentForm(request.POST)
        if form.is_valid():
            peer_assessment = form.save(commit=False)
            peer_assessment.creator = request.user
            peer_assessment.course_id = course_pk
            peer_assessment.save()
            return redirect("edit_assessment", pk=peer_assessment.id, course_pk = course_pk)
    else:
        form = PeerAssessmentForm()

    return render(request, "assessments/create_assessment.html", {"form": form, "course_pk": course_pk})

@login_required
def edit_assessment(request, pk, course_pk):
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

        print(student_emails)

        host = request.get_host()
        public_path = reverse("start_assessment", args=[pk])
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
        return render(request, "assessments/edit_assessment.html", {"peer_assessment": peer_assessment, "questions": questions, "frees":frees, "course_pk": course_pk})

@login_required
def delete_assessment(request, pk):
    peer_assessment = get_object_or_404(PeerAssessment, pk=pk, creator=request.user)
    if request.method == "POST":
        peer_assessment.delete()

    return redirect("")

@login_required
def create_question(request, pk, course_pk):
    peer_assessment = get_object_or_404(PeerAssessment, pk=pk)#, creator=request.user)
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.peer_assessment = peer_assessment
            question.save()
            return redirect("create_options", peer_assessment_pk=pk, question_pk=question.pk,course_pk = course_pk)
    else:
        form = QuestionForm()

    return render(request, "assessments/create_question.html", {"peer_assessment": peer_assessment, "form": form, "course_pk": course_pk})

@login_required
def create_options(request, peer_assessment_pk, question_pk,course_pk):

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
        "peer_assessment": peer_assessment, "question": question, "options": options, "form": form, "course_pk":course_pk
        },
    )

@login_required
def create_free_response(request, peer_assessment_pk,course_pk):
    peer_assessment = get_object_or_404(PeerAssessment, pk=peer_assessment_pk, creator=request.user)
    if request.method == 'POST':
        form = FreeResponseForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.peer_assessment = peer_assessment
            question.save()
            print("valid form saved")
            return redirect("edit_assessment", pk=peer_assessment.pk, course_pk = course_pk)

    else: 
        form = FreeResponseForm()
        print("INVALID")
    return render(request, "assessments/create_free_response.html", {
        "peer_assessment": peer_assessment,  "form": form ,"course_pk": course_pk} #, "question": question, "options": response, "form": form},
    )        

@login_required
def assessments_list(request,course_pk):
    peer_assessments = PeerAssessment.objects.filter(creator=request.user).order_by("-creation_date").all()
    curr = Course.objects.get(course_id=course_pk)
    data = {
        "course_list": get_user_registrations(request),
        "invitations": get_user_invitations(request),
        "peer_assessments": peer_assessments,
        "current_course_name": curr.name,
        "course_pk": course_pk
    }
    return render(request, "assessments/assessments_list.html", data)

@login_required
def start_assessment(request, peer_assessment_pk):
    peer_assessment = get_object_or_404(PeerAssessment, pk=peer_assessment_pk, is_active=True)
    if peer_assessment.end_date < timezone.now():
        peer_assessment.is_active = False
        print("after end date")
        return redirect("home")
    if request.method == "POST":
        form = SubmissionForm(request.POST)
        if form.is_valid():
            sub = form.save(commit=False)
            sub.peer_assessment = peer_assessment
            sub.save()
            print("valid form saved")
            return redirect("submit_assessment", peer_assessment_pk=peer_assessment_pk, sub_pk=sub.pk)
    else: 
        form = SubmissionForm()

    return render(request, "assessments/start_assessment.html", {"peer_assessment": peer_assessment, "form": form})
    
@login_required
def submit_assessment(request, peer_assessment_pk, sub_pk):
    try:
        peer_assessment = PeerAssessment.objects.prefetch_related("question_set__option_set").get(
            pk=peer_assessment_pk, is_active=True
        )
    except PeerAssessment.DoesNotExist:
        raise Http404()

    try:
        sub = peer_assessment.submission_set.get(pk=sub_pk, is_complete=False)
    except Submission.DoesNotExist:
        raise Http404()

    freeresponses = peer_assessment.freeresponse_set.all()
    questions = peer_assessment.question_set.all()
    options = [q.option_set.all() for q in questions]
    form_kwargs = {"empty_permitted": False, "options": options}

    AnswerFormSet = formset_factory(AnswerForm, extra=len(questions), formset=BaseAnswerFormSet)
    freeResponsesFormSet = formset_factory(FreeResponseAnswerForm, extra = len(freeresponses))

    if request.method == "POST":
        formset = AnswerFormSet(request.POST, form_kwargs=form_kwargs)
        freeformset = freeResponsesFormSet()
        if formset.is_valid():
            with transaction.atomic():
                for form in formset:
                    Answer.objects.create(option_id=form.cleaned_data["option"], submission_id=sub_pk)
                for form2 in freeformset:
                    freeresponse = form2.save(commit=False)
                    freeresponse.submission = sub
                    freeresponse.save()
                    print("here")

                sub.is_complete = True
                sub.save()

            return redirect("home")
        else:
            print("notvalid")

    else:
        formset = AnswerFormSet(form_kwargs=form_kwargs)
        freeformset = freeResponsesFormSet()

    question_forms = zip(questions, formset)
    free_forms = zip(freeresponses, freeformset)
    print(len(freeresponses), len(freeformset))
    return render(
        request,
        "assessments/submit_assessment.html",
        {"peer_assessment": peer_assessment, "question_forms": question_forms, "formset": formset, "free_forms": free_forms, "freeformset": freeformset},
    )

def get_user_registrations(request):
    if request.user.is_staff:
        registrations = Course.objects.filter(professor=request.user.email)
    else:
        registrations = Registration.objects.filter(student=request.user.email)
    return registrations

def get_user_invitations(request):
    invitations = []
    if not request.user.is_staff:
        invitations = Invitation.objects.filter(student=request.user.email)
    return invitations
