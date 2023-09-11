from django.http import FileResponse, Http404, JsonResponse
from rest_framework.views import APIView
from django.http import HttpResponse
import os
import pdfkit
import pymysql
from django.http import FileResponse, Http404
from django.template import loader
from datetime import datetime,timedelta
from http.client import responses
from rest_framework.response import Response
from rest_framework import status
from .models import *
from django.template.loader import get_template
from django.shortcuts import render

# Define your database configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "pdf_db"
}

# PDF generation options
pdf_options = {
    'page-size': 'A4',
    'margin-top': '0mm',
    'margin-right': '0mm',
    'margin-bottom': '0mm',
    'margin-left': '0mm',
    'enable-local-file-access': '',
}

# Output directory
output_directory = 'folder1'
output_directory2 = 'folder2'




class GeneratePdf2(APIView):
    
    def post(self, request):
        block = request.data.get("block")
        
        # Establish a database connection
        connection = pymysql.connect(**db_config)
        
        try:
            cursor = connection.cursor()

            # Construct the SQL query
            sql_query = f"SELECT id, name, post, block, dist FROM dom_pdf WHERE block = %s"
            cursor.execute(sql_query, (block,))

            results = cursor.fetchall()

            # Check if there are results
            if not results:
                return Response({"message": "No data found for the given block"}, status=status.HTTP_404_NOT_FOUND)

            # Load the HTML template from the 'templates' directory
            template = loader.get_template('index.html')

            # Create a list to store generated PDF paths
            pdf_paths = []

            for result in results:
                # Check if the PDF already exists for this record
                existing_pdf = Invitation.objects.filter(id=result[0]).values_list('pdf_1', flat=True).first()
                
                if existing_pdf:
                    pdf_paths.append(existing_pdf)
                else:
                    data = {
                        "name": result[1], 
                        "post": result[2],
                        "block": result[3],
                        "dist": result[4]
                    }

                    html_output = template.render(data)

                    # Generate PDF filename based on name and place it in the 'folder1' directory
                    pdf_filename = os.path.join(output_directory, f'{result[1]}.pdf')

                    # Generate PDF only if it doesn't already exist
                    if not os.path.exists(pdf_filename):
                        pdfkit.from_string(html_output, pdf_filename, options=pdf_options)

                    pdf_paths.append(pdf_filename)

                    # Update the corresponding database entry with the PDF path using Django ORM
                    try:
                        invitation_instance = Invitation.objects.get(id=result[0])
                        invitation_instance.pdf_1 = pdf_filename
                        invitation_instance.save()
                    except Invitation.DoesNotExist:
                        pass  # Handle the case where the entry does not exist

                    print(f"PDF for {result[1]} generated successfully as {pdf_filename}")

            

            sql_query = f"SELECT id, name, contact_no, block, dist, post, pdf_1,pdf_2  FROM dom_pdf WHERE block = %s"
            cursor.execute(sql_query,(block,))

            results = cursor.fetchall()

            if not results:
                return Response({"message": "No data found for the given block"}, status=status.HTTP_404_NOT_FOUND)

            template = loader.get_template('index2.html')

            pdf_paths = []


            for result in results:
                # Check if the PDF already exists for this record
                existing_pdf = Invitation.objects.filter(id=result[0]).values_list('pdf_2', flat=True).first()
                
                if existing_pdf:
                    pdf_paths.append(existing_pdf)
                else:
                    data = {
                        "name": result[1], 
                        "contact": result[2],
                        "block": result[3],
                        "dist": result[4],
                        "post": result[5],
                    }

                    html_output = template.render(data)

                    # Generate PDF filename based on name and place it in the 'folder1' directory
                    pdf_filename = os.path.join(output_directory2, f'{result[1]}.pdf')

                    # Generate PDF only if it doesn't already exist
                    if not os.path.exists(pdf_filename):
                        pdfkit.from_string(html_output, pdf_filename, options=pdf_options)

                    pdf_paths.append(pdf_filename)

                    # Update the corresponding database entry with the PDF path using Django ORM
                    try:
                        invitation_instance = Invitation.objects.get(id=result[0])
                        invitation_instance.pdf_2 = pdf_filename
                        invitation_instance.save()
                    except Invitation.DoesNotExist:
                        pass  # Handle the case where the entry does not exist

                    print(f"PDF2 for {result[1]} generated successfully as {pdf_filename}")
            
            result = Invitation.objects.filter(block=block).values()

            return Response({"message": "PDFs generated successfully", "pdf_paths": pdf_paths, "data": result}, status=status.HTTP_200_OK)

        finally:
            cursor.close()
            connection.close()


class DownloadPdf(APIView):
    
    def get(self, request, pdf_name):
        # Construct the full path to the PDF file
        pdf_path = os.path.join(output_directory, pdf_name)

        # Check if the PDF file exists
        if os.path.exists(pdf_path):
            # Open the PDF file for download
            with open(pdf_path, 'rb') as pdf_file:
                response = HttpResponse(pdf_file.read(), content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename="{pdf_name}"'
                return response
        else:
            # If the PDF file doesn't exist, raise an Http404 exception
            raise Http404("PDF not found")


class DownloadPdf2(APIView):
    
    def get(self, request, pdf_name):
        # Construct the full path to the PDF file
        pdf_path = os.path.join(output_directory2, pdf_name)

        # Check if the PDF file exists
        if os.path.exists(pdf_path):
            # Open the PDF file for download
            with open(pdf_path, 'rb') as pdf_file:
                response = HttpResponse(pdf_file.read(), content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename="{pdf_name}"'
                return response
        else:
            # If the PDF file doesn't exist, raise an Http404 exception
            raise Http404("PDF not found")


