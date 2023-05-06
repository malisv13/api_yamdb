from csv import DictReader

from django.conf import settings
from django.http import HttpResponse
from django.db import models
from rest_framework.decorators import action


class CsvImportMixin:

    filename_to_import: str
    import_model: models.Model.__class__

    @action(detail=False, methods=['GET'])
    def import_csv(self, *args, **kwargs):
        csv_files_main_path = settings.BASE_DIR.joinpath('static/data')
        rows_to_create = []

        with open(csv_files_main_path.joinpath(self.filename_to_import), encoding='utf-8') as file:
            for row in DictReader(file):
                rows_to_create.append(
                    self.import_model(
                        **row
                    )
                )

        self.import_model.objects.bulk_create(rows_to_create)

        return HttpResponse('Success import')
