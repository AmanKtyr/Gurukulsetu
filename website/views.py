from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta

def landing_page(request):
    """
    View for the landing page of Gurukul Setu
    """
    # If user is already authenticated, redirect to dashboard
    if request.user.is_authenticated:
        return redirect('home')

    return render(request, 'website/landing_page.html')

def about(request):
    """
    View for the about page
    """
    return render(request, 'website/about.html')

def features(request):
    """
    View for the features page
    """
    return render(request, 'website/features.html')

def contact(request):
    """
    View for the contact page
    """
    return render(request, 'website/contact.html')

def pricing(request):
    """
    View for the pricing page
    """
    return render(request, 'website/pricing.html')

def blog(request):
    """
    View for the blog listing page
    """
    return render(request, 'website/blog.html')

def blog_detail(request, blog_id):
    """
    View for the blog detail page
    """
    # In a real application, you would fetch the blog post from the database
    # For now, we'll just render the template
    return render(request, 'website/blog_detail.html')

def demo(request):
    """
    View for the demo request page
    """
    # Calculate tomorrow's date for the demo request form
    tomorrow_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    context = {
        'tomorrow_date': tomorrow_date
    }
    return render(request, 'website/demo.html', context)
