from django.shortcuts import render
from benford.models import ObservedDataAnalyzer


def home(request):
    context = {}
    context['accepted_formats'] = ".csv, .txt"
    return render(request, "home.html", context)


def results(request):
    if request.method != "POST" or "user_file" not in request.FILES:
        error_context = {}
        return render(request, "error.html", error_context)

    BL_analysis = ObservedDataAnalyzer(request.FILES['user_file'])

    if not BL_analysis.is_data_valid():
        error_context = {}
        error_context['error_message'] = BL_analysis.error_message
        return render(request, "error.html", error_context)

    context = {}
    context['BL_analysis'] = BL_analysis
    return render(request, "results.html", context)
