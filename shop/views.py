from django.shortcuts import render


def start_page(request):
    return render(request, 'start-page.html')