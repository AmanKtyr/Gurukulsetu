from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def landing_page(request):
    """
    View for the landing page of Gurukul Setu
    """
    # If user is already authenticated, redirect to dashboard
    if request.user.is_authenticated:
        return redirect('home')
    
    return render(request, 'website/landing_page.html')
