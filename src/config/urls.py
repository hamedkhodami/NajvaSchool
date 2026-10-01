from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("apps.account.urls", namespace="account")),
    path("student/", include("apps.student.urls", namespace="student")),
    path("teacher/", include("apps.teacher.urls", namespace="teacher")),
    path("academic/", include("apps.academic.urls", namespace="academic")),
    path("attendance/", include("apps.attendance.urls", namespace="attendance")),
    path("education/", include("apps.education.urls", namespace="education")),
    path("discipline/", include("apps.discipline.urls", namespace="discipline")),
    path("finance/", include("apps.finance.urls", namespace="finance")),
    path("payment/", include("apps.payment.urls", namespace="payment")),
    path("notification/", include("apps.notification.urls", namespace="notification")),
    path("", include("apps.public.urls", namespace="public")),
    path("dashboard/", include("apps.dashboard.urls", namespace="dashboard")),
]

# --- Static files ---
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# --- Media files ---
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
