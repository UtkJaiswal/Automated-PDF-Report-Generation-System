from django.db import models

# Create your models here.
class Invitation(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    contact_no = models.CharField(max_length=255, blank=True, null= True)
    block = models.CharField(max_length=255, blank= True, null=True)
    dist = models.CharField(max_length=255, blank=True, null=True)
    post = models.CharField(max_length=255, blank=True, null=True)
    pdf_1 = models.CharField(max_length=255, blank=True, null=True)
    pdf_2 = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dom_pdf'