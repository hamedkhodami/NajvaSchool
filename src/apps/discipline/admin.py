from django.contrib import admin

from apps.discipline.models import (
    BehavioralEvaluationModel,
    DisciplineRecordModel,
    DisciplineTypeModel,
    EducationalRecordModel,
)


@admin.register(DisciplineTypeModel)
class DisciplineTypeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "effect",
        "is_active",
        "created_at",
    )

    list_display_links = (
        "id",
        "name",
    )

    list_filter = (
        "effect",
        "is_active",
    )

    search_fields = (
        "name",
        "description",
    )

    ordering = ("name",)

    readonly_fields = (
        "created_at",
        "updated_at",
    )


@admin.register(DisciplineRecordModel)
class DisciplineRecordAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "student",
        "discipline_type",
        "recorder",
        "classroom",
        "date",
        "title",
    )

    list_display_links = (
        "id",
        "student",
        "title",
    )

    list_filter = (
        "discipline_type__effect",
        "date",
        "classroom",
    )

    search_fields = (
        "student__user__first_name",
        "student__user__last_name",
        "student__national_id",
        "title",
        "description",
    )

    autocomplete_fields = (
        "student",
        "discipline_type",
        "recorder",
        "classroom",
    )

    date_hierarchy = "date"

    ordering = (
        "-date",
        "-created_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )


@admin.register(BehavioralEvaluationModel)
class BehavioralEvaluationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "student",
        "title",
        "level",
        "evaluator",
        "classroom",
        "evaluation_date",
    )

    list_display_links = (
        "id",
        "student",
        "title",
    )

    list_filter = (
        "level",
        "evaluation_date",
        "classroom",
    )

    search_fields = (
        "student__user__first_name",
        "student__user__last_name",
        "student__national_id",
        "title",
        "description",
    )

    autocomplete_fields = (
        "student",
        "evaluator",
        "classroom",
    )

    date_hierarchy = "evaluation_date"

    ordering = (
        "-evaluation_date",
        "-created_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )


@admin.register(EducationalRecordModel)
class EducationalRecordAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "student",
        "record_type",
        "title",
        "recorder",
        "classroom",
        "date",
    )

    list_display_links = (
        "id",
        "student",
        "title",
    )

    list_filter = (
        "record_type",
        "date",
        "classroom",
    )

    search_fields = (
        "student__user__first_name",
        "student__user__last_name",
        "student__national_id",
        "title",
        "description",
    )

    autocomplete_fields = (
        "student",
        "recorder",
        "classroom",
    )

    date_hierarchy = "date"

    ordering = (
        "-date",
        "-created_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )
