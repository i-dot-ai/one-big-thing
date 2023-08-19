"""
Views for info pages like privacy notice, accessibility statement, etc.
These shouldn't contain sensitive data and don't require login.
"""

from django.views.decorators.http import require_http_methods
from django.shortcuts import render


@require_http_methods(["GET"])
def privacy_notice_view(request):
    return render(request, "privacy-notice.html", {})


@require_http_methods(["GET"])
def support_view(request):
    return render(request, "support.html", {})


@require_http_methods(["GET"])
def accessibility_statement_view(request):
    return render(request, "accessibility-statement.html", {})
