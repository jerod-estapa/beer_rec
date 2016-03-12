from django.contrib import admin

from .models import Beer, Review


class ReviewAdmin(admin.ModelAdmin):
    model = Review
    list_display = ('beer', 'rating', 'user_name', 'comment', 'pub_date')
    list_filter = ['pub_date', 'user_name']
    search_fields = ['comment']

admin.site.register(Beer)
admin.site.register(Review, ReviewAdmin)
