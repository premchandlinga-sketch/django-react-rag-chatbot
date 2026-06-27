import os
import shutil

from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from chatbot.models import UploadedDocument
from chatbot.services.vector_store_service import VectorStoreService


class UploadedDocumentAPIView(APIView):

    def delete(self, request, document_id):
        try:
            document = UploadedDocument.objects.get(id=document_id)
        except UploadedDocument.DoesNotExist:
            return Response(
                {"error": "Document not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Delete physical file
        pdf_path = os.path.join(settings.BASE_DIR, "uploads", document.file_name)
        if os.path.exists(pdf_path):
            try:
                os.remove(pdf_path)
            except Exception as e:
                print(f"Warning: Could not delete file {pdf_path}: {e}")

        # Get session to delete from vector store
        session = document.session

        # Delete document from vector store
        if session and session.collection_name:
            VectorStoreService.delete_document_from_vector_store(
                session.collection_name, 
                document.file_name
            )

        # Delete from database
        document.delete()

        return Response({
            "message": "Document deleted successfully"
        })