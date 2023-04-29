import os

from django.http import HttpResponse
from csv import DictReader
from django.conf import settings


def import_csv_to_database(request):
    csv_files_main_path = settings.BASE_DIR.joinpath('static/data')
    csv_files_paths = os.listdir(csv_files_main_path)

    for csv_file in csv_files_paths:
        with open(csv_files_main_path.joinpath(csv_file), encoding='utf-8') as file:
            for row in DictReader(file):
                print(type(row))

    return HttpResponse('Success import')



"""for row in DictReader(open('./children.csv')):
    print(row)"""
