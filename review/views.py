from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .models import Review
from .forms import ReviewForm

# Create your views here.

def submit_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('reviews_list')
    else:
        form = ReviewForm()
    return render(request, 'review/submit_review.html', {'form': form})

def reviews_list(request):
    reviews = Review.objects.all().order_by('-created_at')
    return render(request, 'review/reviews_list.html', {'reviews': reviews})



def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def post_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('reviews_list')
    else:
        form = ReviewForm()
    return render(request, 'review/post_review.html', {'form': form})