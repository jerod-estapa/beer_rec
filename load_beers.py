# -*- coding: utf-8 -*-

""" This script loads beers from the database. """

import sys, os
import pandas as pd

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "beer_rec.settings")

import django
django.setup()

from reviews.models import Beer


def save_beer_from_row(beer_row):
    beer = Beer()
    beer.id = beer_row[0]
    beer.username = beer_row[1]
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
