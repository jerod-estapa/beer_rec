# Reviews App - Views

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .models import Review, Beer
from .forms import ReviewForm
import datetime


def review_list(request):
    latest_review_list = Review.objects.order_by('-pub_date')[:9]
    context = {'latest_review_list': latest_review_list}
    return render(request, 'reviews/review_list.html', context)


def review_detail(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    return render(request, 'reviews/review_detail.html', {'review': review})


def beer_list(request):
    ordered_beer_list = Beer.objects.order_by('-name')
    context = {'ordered_beer_list': ordered_beer_list}
    return render(request, 'reviews/beer_list.html', context)


def beer_detail(request, beer_id):
    beer = get_object_or_404(Beer, pk=beer_id)
    form = ReviewForm()
    return render(request, 'reviews/beer_detail.html', {'beer': beer, 'form': form})


def add_review(request, beer_id):
    beer = get_object_or_404(Beer, pk=beer_id)
    form = ReviewForm(request.POST)
    if form.is_valid():
        rating = form.cleaned_data['rating']
        comment = form.cleaned_data['comment']
        user_name = form.cleaned_data['user_name']
        review = Review()
        review.beer = beer
        review.user_name = user_name
        review.rating = rating
        review.comment = comment
        review.pub_date = datetime.datetime.now()
        review.save()
        # HttpResponseRedirect used here to prevent user
        # from posting data twice by hitting Back button
        return HttpResponseRedirect(reverse('reviews:beer_detail', args=(beer.id,)))

    return render(request, 'reviews/beer_detail.html', {'beer': beer, 'form': form})
