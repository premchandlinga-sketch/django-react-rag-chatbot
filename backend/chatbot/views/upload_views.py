import os

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from chatbot.models import ChatSession

from chatbot.services.document_service import (
    DocumentService
)

from chatbot.services.vector_store_service import (
    VectorStoreService
)


class UploadPDFAPIView(APIView):

    def post(self, request):

        pdf_file = request.FILES.get("file")

        session_id = request.data.get(
            "session_id"
        )

        if not pdf_file:

            return Response(
                {
                    "error": "No file uploaded"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if not session_id:

            return Response(
                {
                    "error":
                    "session_id is required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:

            session = ChatSession.objects.get(
                id=session_id
            )

        except ChatSession.DoesNotExist:

            return Response(
                {
                    "error":
                    "Session not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        upload_dir = os.path.join(
            settings.BASE_DIR,
            "uploads"
        )

        os.makedirs(
            upload_dir,
            exist_ok=True
        )

        upload_path = os.path.join(
            upload_dir,
            pdf_file.name
        )

        with open(
            upload_path,
            "wb+"
        ) as destination:

            for chunk in pdf_file.chunks():

                destination.write(
                    chunk
                )

        documents = (
            DocumentService.load_pdf(
                upload_path
            )
        )

        chunks = (
            DocumentService.split_documents(
                documents
            )
        )

        if not session.collection_name:

            session.collection_name = (
                f"session_{session.id}"
            )

            session.save()

        VectorStoreService.create_vector_store(
            chunks,
            session.collection_name
        )

        return Response(
            {
                "message":
                "PDF uploaded successfully",

                "collection":
                session.collection_name,

                "chunks":
                len(chunks)
            }
        )