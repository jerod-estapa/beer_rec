from django.shortcuts import get_object_or_404, render

from .models import Review, Beer


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
    return render(request, 'reviews/beer_detail.html', {'beer': beer})
