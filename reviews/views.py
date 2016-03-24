# Reviews App - Views

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Review, Beer, Cluster
from .forms import ReviewForm
from .suggestions import update_clusters
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


@login_required
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
        update_clusters()
        # HttpResponseRedirect used here to prevent user
        # from posting data twice by hitting Back button
        return HttpResponseRedirect(reverse('reviews:beer_detail', args=(beer.id,)))

    return render(request, 'reviews/beer_detail.html', {'beer': beer, 'form': form})


def user_review_list(request, username=None):
    if not username:
        username = request.user.username
    latest_review_list = Review.objects.filter(user_name=username).order_by('-pub_date')
    context = {'latest_review_list': latest_review_list, 'username': username}
    return render(request, 'reviews/user_review_list.html', context)


@login_required
def user_recommendation_list(request):

    # Get this user's reviews and a set of beer IDs
    user_reviews = Review.objects.filter(user_name=request.user.username).prefetch_related('beer')
    user_reviews_beer_ids = list(map(lambda x: x.beer.id, user_reviews))

    # Get request user cluster name (just the first one)
    try:
        user_cluster_name = \
            User.objects.get(username=request.user.username).cluster_set.first().name
    except:
        update_clusters()
        user_cluster_name = \
            User.objects.get(username=request.user.username).cluster_set.first().name

    # Get usernames for other members in the cluster
    user_cluster_other_members = \
        Cluster.objects.get(name=user_cluster_name).users.exclude(request.user.username).all()
    other_members_usernames = set(map(lambda x: x.username, user_cluster_other_members))

    # Get reviews by those members, excluding beers reviewed by the request user
    other_users_reviews = \
        Review.objects.filter(user_name__in=other_members_usernames) \
        .exclude(beer__id__in=user_reviews_beer_ids)
    other_users_reviews_beer_ids = set(map(lambda x: x.beer.id, other_users_reviews))

    # Then, get a beer list including the previous IDs, ordered by rating
    user_beer_list = sorted(
        list(Beer.objects.filter(id__in=other_users_reviews_beer_ids)),
        key=lambda x: x.average_rating(),
        reverse=True
    )

    return render(
        request,
        'reviews/user_recommendation_list.html',
        {'username': request.user.username, 'user_beer_list': user_beer_list}
    )
