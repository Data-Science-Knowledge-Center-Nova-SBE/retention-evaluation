import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from rest_framework.authtoken.models import Token

from apps.web.management.models import LogActivity, ProjectState
from apps.web.management.reset import change_models_to_default

from apps.web.management import mockup
from apps.web.management.predict_utils import transform_predictions


@login_required(login_url='/authsite/login')
def home(request):
    token, created = Token.objects.get_or_create(user=request.user)

    context = {}
    context["apiKey"] = token.key

    return render(request, 'management/api.html', context)


@login_required(login_url='/authsite/login')
def api(request):
    if request.method == "POST":
        token, created = Token.objects.get_or_create(user=request.user)
        token.delete()

    token, created = Token.objects.get_or_create(user=request.user)

    context = {}
    context["apiKey"] = token.key

    return render(request, 'management/api.html', context)


def call_api(request, url, data):
    token, _ = Token.objects.get_or_create(user=request.user)
    response = requests.post(url, json=data, headers={'Authorization': 'Token ' + token.key})

    return response.json()


@login_required(login_url='/authsite/login')
def predict(request, grade='9', k=20):
    # create context
    context = {}
    context["k"] = k
    context["grade"] = grade

    # get mockup data
    mockup_data = mockup.get_mockup_data(grade=grade)[:50]

    # test api
    url = request.build_absolute_uri(reverse('prediction-' + grade + '-grade'))
    data = call_api(request, url, mockup_data)

    # add names
    data = mockup.add_random_names(data)
    context["predictions"] = transform_predictions(data, k)

    return render(request, 'management/predict.html', context);


def error_request(request, context, name):
    context["error"] = True
    context["error_" + name] = True
    return render(request, 'management/predict.html', context);


@login_required(login_url='/authsite/login')
def reset(request):
    token, created = Token.objects.get_or_create(user=request.user)

    change_models_to_default()

    # create state
    state, _ = ProjectState.objects.get_or_create()
    state.delete()

    # create a new project state
    state = ProjectState.objects.create()
    state.trained = True

    # log
    LogActivity.objects.create(type=LogActivity.LOG_RESET, description="Reset train")

    context = {}
    context["state"] = state
    context["apiKey"] = token.key

    return redirect("management.home");


@login_required(login_url='/authsite/login')
def logs(request):
    context = {}
    context["logs"] = LogActivity.objects.all().order_by("-timestamp")

    return render(request, 'management/logs.html', context);
