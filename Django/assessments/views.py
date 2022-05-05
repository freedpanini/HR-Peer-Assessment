
#<<<<<<< HEAD

# Create your views here.

#=======
from django.shortcuts import render, redirect, get_object_or_404
from .models import FreeResponse, FreeResponseAnswer, PeerAssessment, Question, Answer, Submission
from courses.models import Course, Registration, Invitation, Team
from .forms import FreeResponseAnswerForm, PeerAssessmentForm, QuestionForm, OptionForm, FreeResponseForm, AnswerForm, BaseAnswerFormSet, SubmissionForm
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from courses.models import Course, Registration
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.forms.formsets import formset_factory
from django.db import transaction
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import Group, User
from django import forms
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

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

    data = {
        "course_list": get_user_registrations(request),
        "invitations": get_user_invitations(request),
        "current_course_name": Course.objects.get(course_id=course_pk).name,
        "current_course": course_pk,
        "form": form, 
        "course_pk": course_pk
    }

    return render(request, "assessments/create_assessment.html", data)

@login_required
def edit_assessment(request, pk, course_pk):
    try:
        peer_assessment = PeerAssessment.objects.prefetch_related("question_set__option_set").get(
            pk=pk, creator=request.user
        )
    except PeerAssessment.DoesNotExist:
        print("Doesnt exist")
        raise Http404()

    try:
        peer_assessment2 = PeerAssessment.objects.prefetch_related("freeresponse_set").get(
            pk=pk, creator=request.user
        )
    except PeerAssessment.DoesNotExist:
        raise Http404()

    questions = peer_assessment.question_set.all()
    frees = peer_assessment2.freeresponse_set.all()
    if request.method == "POST":
        if 'publish_results' in request.POST:
            peer_assessment.is_published = True
            peer_assessment.save()

            emails = []
            registrations= Registration.objects.filter(course_id = course_pk)

            for r in registrations:
                emails.append(r.student)
            print(emails)

            print("RESULTS PUBLISHED")
            registered = Registration.objects.filter(course_id = data['current_course'])
            emails = []
            for r in registered:
                emails.append(r.student)

            if emails is None or len(emails) == 0:
                return render(request, "assessments/assessment_results.html", data)

            results_published_email(request, emails, data['current_course_name'])
            return redirect("home")
        if 'activate_assessment' in request.POST:
            registered = Registration.objects.filter(course_id = data['course_pk'])
            emails = []
            for r in registered:
                emails.append(r.student)

            if emails is None or len(emails) == 0:
                return render(request, "assessments/create_assessment.html", data)

            assessment_release_email(request, emails, data['current_course_name'])
            print("ACTIVATED ASSESSMENTS")
            peer_assessment.is_active = True
            peer_assessment.save()
            course = Course.objects.get(course_id=peer_assessment.course_id)
            registrations = Registration.objects.filter(course_id=course.course_id)
            student_emails = [o.student for o in registrations]

            return redirect("home")
        else:
            print("here")
            return HttpResponse()
    else:
        data = {
            "course_list": get_user_registrations(request),
            "invitations": get_user_invitations(request),
            "current_course_name": Course.objects.get(course_id=course_pk).name,
            "peer_assessment": peer_assessment, 
            "questions": questions, 
            "current_course": course_pk,
            "frees":frees, 
            "course_pk": course_pk
        }
        
        return render(request, "assessments/edit_assessment.html", data)

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
    data = {
        "course_list": get_user_registrations(request),
        "invitations": get_user_invitations(request),
        "current_course": course_pk,
        "current_course_name": Course.objects.get(course_id=course_pk).name,
        "peer_assessment": peer_assessment, 
        "form": form, 
        "course_pk": course_pk
    }
    return render(request, "assessments/create_question.html", data)

@login_required
def create_options(request, peer_assessment_pk, question_pk,course_pk):

    peer_assessment = get_object_or_404(PeerAssessment, pk=peer_assessment_pk, creator=request.user)
    question = Question.objects.get(pk=question_pk)
    if request.method == "POST":
        form = OptionForm(request.POST)
        if form.is_valid():
            option = form.save(commit=False)
            option.question_id = question_pk
            print(option.value)
            option.save()
    else:
        form = OptionForm()

    options = question.option_set.all()
    data = {
        "course_list": get_user_registrations(request),
        "invitations": get_user_invitations(request),
        "current_course": course_pk,
        "current_course_name": Course.objects.get(course_id=course_pk).name,
        "peer_assessment": peer_assessment, 
        "question": question, 
        "options": options, 
        "form": form, 
        "course_pk":course_pk
    }
    return render(request, "assessments/create_options.html", data)

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

    data = {
        "course_list": get_user_registrations(request),
        "invitations": get_user_invitations(request),
        "current_course": course_pk,
        "current_course_name": Course.objects.get(course_id=course_pk).name,
        "peer_assessment": peer_assessment,  
        "form": form ,
        "course_pk": course_pk
    }
    #, "question": question, "options": response, "form": form},
    return render(request, "assessments/create_free_response.html", data)        

@login_required
def assessments_list(request,course_pk):
    peer_assessments = PeerAssessment.objects.filter(creator=request.user).filter(course_id=course_pk).order_by("-creation_date").all()
    curr = Course.objects.get(course_id=course_pk)
    data = {
        "course_list": get_user_registrations(request),
        "invitations": get_user_invitations(request),
        "peer_assessments": peer_assessments,
        "current_course_name": curr.name,
        "course_pk": course_pk,
        "user": request.user
    }
    return render(request, "assessments/assessments_list.html", data)

@login_required
def start_assessment(request, peer_assessment_pk,course_pk):
    peer_assessment = get_object_or_404(PeerAssessment, pk=peer_assessment_pk, is_active=True)
    groups = request.user.groups.all()
    groupmates = User.objects.all()

    for g in groups:
        print(g.name)
        groupmates = User.objects.filter(groups__name=g.name)

    if peer_assessment.end_date < timezone.now():
        peer_assessment.is_active = False
        print("after end date")
        return redirect("assessment_results", peer_assessment_pk=peer_assessment_pk, course_pk=course_pk)
    if request.method == "POST":
        form = SubmissionForm(request.POST)
        form.assigned_to = forms.ModelChoiceField(queryset=groupmates)
        if form.is_valid():
            if Submission.objects.filter(assigned_to = form.cleaned_data["assigned_to"]).filter(submitted_by = request.user).filter(peer_assessment= peer_assessment).exists():
                Submission.objects.filter(assigned_to = form.cleaned_data["assigned_to"]).filter(submitted_by = request.user).filter(peer_assessment= peer_assessment).delete()
                print("updated")
            sub = form.save(commit=False)
            sub.peer_assessment = peer_assessment
            sub.submitted_by = request.user
            sub.save()
            return redirect("submit_assessment", peer_assessment_pk=peer_assessment_pk, sub_pk=sub.pk, course_pk = course_pk)
    else:
        form = SubmissionForm()
        form.assigned_to = forms.ModelChoiceField(queryset=groupmates)

    data = {
        "course_list": get_user_registrations(request),
        "invitations": get_user_invitations(request),
        "current_course": course_pk,
        "current_course_name": Course.objects.get(course_id=course_pk).name,
        "peer_assessment": peer_assessment, 
        "form": form
    }

    return render(request, "assessments/start_assessment.html", data)
    
@login_required
def submit_assessment(request, peer_assessment_pk, sub_pk, course_pk):
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

    #create formsets for MCs and free responses
    AnswerFormSet = formset_factory(AnswerForm, extra=len(questions), formset=BaseAnswerFormSet)
    freeResponsesFormSet = formset_factory(FreeResponseAnswerForm, extra = len(freeresponses))

    
    if request.method == "POST":

        #tried initial but didnt work
        formset = AnswerFormSet(request.POST, form_kwargs=form_kwargs,prefix="mcForms")
        freeformset = freeResponsesFormSet(initial = [{'response_answer': 'test'}], prefix="freeForms")

        if formset.is_valid() and freeformset.is_valid():
            print("MC valid")
            with transaction.atomic():
                for form in formset:
                    Answer.objects.create(option_id=form.cleaned_data["option"], submission_id=sub_pk)

            print("frees valid")
            for form2 in freeformset:
                #freeformset is never valid because there is no data in text boxes 
                #these prints wont print anything
                print("FREE RESPONSE:", form2.cleaned_data["response_answer"])
                freeresponse = form2.save(commit=False)
                print("FREE RESPONSE2:", freeresponse.response_answer)                   
                freeresponse.free_response = FreeResponse.objects.get(pk = freeresponses[0].pk)
                freeresponse.submission = sub
                freeresponse.save()
        else:
            print("notvalid")
            print("ERRORS",freeformset.errors)

        sub.is_complete = True
        sub.save()

        return redirect("home")
        

    else:
        formset = AnswerFormSet(form_kwargs=form_kwargs, prefix="mcForms")
        freeformset = freeResponsesFormSet(prefix="freeForms")


    question_forms = zip(questions, formset)
    free_forms = zip(freeresponses, freeformset)


    data = {
        "course_list": get_user_registrations(request),
        "invitations": get_user_invitations(request),
        "current_course": course_pk,
        "current_course_name": Course.objects.get(course_id=course_pk).name,
        "peer_assessment": peer_assessment, 
        "question_forms": question_forms, 
        "freeresponses": freeresponses,
        "formset": formset,
        "free_forms": free_forms, 
        "freeformset": freeformset
    }
    return render(request, "assessments/submit_assessment.html", data)

def assessment_results(request, peer_assessment_pk, course_pk):
    submissions = Submission.objects.filter(assigned_to=request.user, peer_assessment=peer_assessment_pk)
    mc_response = {}  #mc_response is a hashmap of hashmaps where questions -> options -> occurrence of each option in submissions
    for submission in submissions:
        answers = Answer.objects.filter(submission=submission)
        for answer in answers:  #collect mc answers
            op = answer.option
            q = op.question
            if q.question in mc_response:
                if op.option_text in mc_response[q.question]:
                    mc_response[q.question][op.option_text] += 1
                else:
                    mc_response[q.question][op.option_text] = 1
            else:
                mc_response[q.question] = {}
                mc_response[q.question][op.option_text] = 1
        fr_answers = FreeResponseAnswer.objects.filter(submission=submission)

        for fr_answer in fr_answers:    #TODO: collect free response answers
            print(fr_answer.response_answer)

    max_responses = {}

    for key, value in mc_response.items():
        max_val = max(value.items(), key=lambda x : x[1])
        max_answers = max_val[0]
        for k, v in value.items():  #handles case where multiple answers are most common
            if k != max_val[0] and v == max_val[1]:
                max_answers += ", " + k
        max_responses[key] = max_answers
    data = {
        "course_list": get_user_registrations(request),
        "invitations": get_user_invitations(request),
        "current_course": course_pk,
        "current_course_name": Course.objects.get(course_id=course_pk).name,
        "mc_response": max_responses
    }

    return render(request, "assessments/assessment_results.html", data)

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

def assessment_release_email(request, emails, name):
    #ctx={
    #    'name':name,
    #}
    message=render_to_string('assessments/assessment_email.html')
    send_mail('The survey is now ready to be filled out',
    message,
    settings.EMAIL_HOST_USER,
    emails,
    fail_silently=False,html_message=message)
    return render(request, 'courses/send_email.html',{})

def results_published_email(request, emails, name):
   #ctx={
   #     'name':name,
   # }
    message=render_to_string('assessments/results_email.html')
    send_mail('The results are now available to view ',
    message,
    settings.EMAIL_HOST_USER,
    emails,
    fail_silently=False,html_message=message)
    return render(request, 'courses/send_email.html',{})




