from import_export import resources

from subjects.models import SubjectCategory, PrimarySubject, SecondarySubject


class SubjectCategoryResource(resources.ModelResource):
    def before_import_row(self, row, **kwargs):
        row["code"] = str(row["code"]).zfill(2)

    class Meta:
        model = SubjectCategory
        import_id_fields = ("code",)


class PrimarySubjectResource(resources.ModelResource):
    def before_import_row(self, row, **kwargs):
        row["code"] = str(row["code"]).zfill(4)
        row["category"] = str(row["category"]).zfill(2)

    class Meta:
        model = PrimarySubject
        import_id_fields = ("code",)


class SecondarySubjectResource(resources.ModelResource):
    def before_import_row(self, row, **kwargs):
        row["code"] = str(row["code"]).zfill(6)
        row["primary_subject"] = str(row["primary_subject"]).zfill(4)

    class Meta:
        model = SecondarySubject
        import_id_fields = ("code",)
