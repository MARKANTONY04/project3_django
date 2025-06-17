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
    return render(request, 'reviews/submit_review.html', {'form': form})

def reviews_list(request):
    reviews = Review.objects.all().order_by('-created_at')
    return render(request, 'reviews/reviews_list.html', {'reviews': reviews})
