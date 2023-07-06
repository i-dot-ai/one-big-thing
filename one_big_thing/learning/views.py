from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from . import models, utils


@login_required
@require_http_methods(["GET"])
def index_view(request):
    return redirect(reverse("homepage"))


@login_required
@require_http_methods(["GET"])
def homepage_view(request):
    courses = models.Course.objects.all()
    data = {"courses": courses}
    errors = {}
    return render(
        request,
        template_name="homepage.html",
        context={
            "request": request,
            "data": data,
            "errors": errors,
        },
    )
