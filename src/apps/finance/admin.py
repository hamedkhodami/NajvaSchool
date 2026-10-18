from django.contrib import admin

from apps.finance.models import (
    PaymentRecordModel,
    SalaryPaymentModel,
    SchoolExpenseModel,
    StaffSalaryModel,
    TuitionModel,
)


@admin.register(TuitionModel)
class TuitionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "student",
        "academic_year",
        "amount",
        "discount",
        "final_amount",  # 🔥 property
        "status",
    )

    list_display_links = ("id", "student")

    list_filter = ("status", "academic_year")

    search_fields = (
        "student__user__first_name",
        "student__user__last_name",
        "student__national_id",
    )

    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)


@admin.register(PaymentRecordModel)
class PaymentRecordAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "student",
        "tuition",
        "amount",
        "payment_method",
    )

    list_display_links = (
        "id",
        "student",
    )

    list_filter = ("payment_method",)

    search_fields = (
        "student__user__first_name",
        "student__user__last_name",
        "student__national_id",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    date_hierarchy = "created_at"

    ordering = ("-created_at",)


@admin.register(StaffSalaryModel)
class StaffSalaryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "teacher",
        "academic_year",
        "base_amount",
    )

    list_display_links = (
        "id",
        "teacher",
    )

    list_filter = ("academic_year",)

    search_fields = (
        "teacher__user__first_name",
        "teacher__user__last_name",
        "teacher__national_id",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = ("created_at",)


@admin.register(SalaryPaymentModel)
class SalaryPaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "salary",
        "amount",
        "payment_date",
    )

    list_display_links = (
        "id",
        "salary",
    )

    list_filter = ("payment_date",)

    search_fields = (
        "salary__teacher__user__first_name",
        "salary__teacher__user__last_name",
        "salary__teacher__national_id",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    date_hierarchy = "payment_date"

    ordering = ("-payment_date",)


@admin.register(SchoolExpenseModel)
class SchoolExpenseAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "amount", "academic_year")
    list_filter = ("category", "academic_year")
    search_fields = ("title", "description")
