
from django.urls import path,include
from .views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    # path('bulk_download/', BulkDownloadView.as_view()),
    # path('abc/', GeneratePdf.as_view()),
    path('abc2/', GeneratePdf2.as_view()),
    path('abc3/<str:pdf_name>/', DownloadPdf.as_view()),
    path('abc4/<str:pdf_name>/', DownloadPdf2.as_view()),
]
