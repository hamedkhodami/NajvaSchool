from django.contrib import admin

from apps.payment.models import PaymentModel


@admin.register(PaymentModel)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "student",
        "tuition",
        "installment",
        "amount",
        "payment_method",
        "status",
        "paid_at",
        "created_at",
    )

    list_display_links = (
        "id",
        "student",
    )

    list_filter = (
        "payment_method",
        "status",
        "paid_at",
        "created_at",
    )

    search_fields = (
        "student__national_id",
        "student__user__first_name",
        "student__user__last_name",
        "student__user__phone_number",
        "tuition__student__national_id",
        "authority",
        "tracking_code",
        "ref_id",
        "card_pan",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        "paid_at",
        "authority",
        "ref_id",
    )

    fieldsets = (
        (
            "اطلاعات پرداخت",
            {
                "fields": (
                    "student",
                    "tuition",
                    "installment",
                    "amount",
                    "payment_method",
                    "status",
                )
            },
        ),
        (
            "اطلاعات تراکنش",
            {
                "fields": (
                    "authority",
                    "tracking_code",
                    "ref_id",
                    "card_pan",
                    "paid_at",
                    "expire_at",
                )
            },
        ),
        (
            "توضیحات",
            {"fields": ("description",)},
        ),
        (
            "تاریخ‌ها",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    ordering = ("-created_at",)

    date_hierarchy = "created_at"
