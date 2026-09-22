from django.contrib import admin

from apps.finance.models import (
    PaymentRecordModel,
    SalaryPaymentModel,
    SchoolExpenseModel,
    StaffSalaryModel,
    TuitionInstallmentModel,
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
        "status",
    )

    list_display_links = (
        "id",
        "student",
    )

    list_filter = (
        "status",
        "academic_year",
    )

    search_fields = (
        "student__user__first_name",
        "student__user__last_name",
        "student__national_id",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = ("-created_at",)


@admin.register(TuitionInstallmentModel)
class TuitionInstallmentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "tuition",
        "installment_number",
        "amount",
        "due_date",
    )

    list_display_links = (
        "id",
        "tuition",
    )

    list_filter = (
        "due_date",
        "tuition__status",
    )

    search_fields = (
        "tuition__student__user__first_name",
        "tuition__student__user__last_name",
        "tuition__student__national_id",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "tuition",
        "installment_number",
    )


@admin.register(PaymentRecordModel)
class PaymentRecordAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "student",
        "tuition",
        "installment",
        "amount",
        "payment_method",
        "status",
        "payment_date",
        "tracking_code",
    )

    list_display_links = (
        "id",
        "student",
    )

    list_filter = (
        "status",
        "payment_method",
        "payment_date",
    )

    search_fields = (
        "student__user__first_name",
        "student__user__last_name",
        "student__national_id",
        "tracking_code",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    date_hierarchy = "payment_date"

    ordering = ("-payment_date",)


@admin.register(StaffSalaryModel)
class StaffSalaryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "teacher",
        "academic_year",
        "year",
        "month",
        "base_amount",
        "bonus_amount",
        "deduction_amount",
        "final_amount",
        "status",
    )

    list_display_links = (
        "id",
        "teacher",
    )

    list_filter = (
        "status",
        "academic_year",
        "year",
        "month",
    )

    search_fields = (
        "teacher__user__first_name",
        "teacher__user__last_name",
        "teacher__national_id",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "-year",
        "-month",
    )


@admin.register(SalaryPaymentModel)
class SalaryPaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "salary",
        "amount",
        "payment_date",
        "payment_method",
        "tracking_code",
    )

    list_display_links = (
        "id",
        "salary",
    )

    list_filter = (
        "payment_method",
        "payment_date",
    )

    search_fields = (
        "salary__teacher__user__first_name",
        "salary__teacher__user__last_name",
        "salary__teacher__national_id",
        "tracking_code",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    date_hierarchy = "payment_date"

    ordering = ("-payment_date",)


@admin.register(SchoolExpenseModel)
class SchoolExpenseAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "category",
        "amount",
        "expense_date",
        "receipt_number",
    )

    list_display_links = (
        "id",
        "title",
    )

    list_filter = (
        "category",
        "expense_date",
    )

    search_fields = (
        "title",
        "receipt_number",
        "description",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    date_hierarchy = "expense_date"

    ordering = ("-expense_date",)
