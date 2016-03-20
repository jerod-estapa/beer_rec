# -*- coding: utf-8 -*-

""" This script loads beers from the database. """

import sys, os
import pandas as pd
import django

from reviews.models import Beer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "beer_rec.settings")
django.setup()


def save_beer_from_row(beer_row):
    beer = beer()
    beer.id = user_row[0]
    beer.username = user_row[1]
    beer.save()


if __name__ == "__main__":

    if len(sys.argv) == 2:
        print("Reading from file " + str(sys.argv[1]))
        beers_df = pd.read_csv(sys.argv[1])
        print(beers_df)

        beers_df.apply(
            save_beer_from_row,
            axis=1
        )

        print("There are {} beers".format(Beer.objects.count()))

    else:
        print("Please, provide Beer file path.")
