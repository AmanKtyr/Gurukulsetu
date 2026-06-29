from django.shortcuts import render

def dashboard(request):
    return render(request, 'communication/dashboard.html')
