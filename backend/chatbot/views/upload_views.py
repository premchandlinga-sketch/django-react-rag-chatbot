import os

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from chatbot.services.document_service import (
    DocumentService
)

from chatbot.services.vector_store_service import (
    VectorStoreService
)


class UploadPDFAPIView(APIView):

    def post(self, request):

        pdf_file = request.FILES.get("file")

        if not pdf_file:

            return Response(
                {
                    "error": "No file uploaded"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        upload_dir = os.path.join(
            settings.BASE_DIR,
            "uploads"
        )

        os.makedirs(
            upload_dir,
            exist_ok=True)

        upload_path = os.path.join(
            upload_dir,
            pdf_file.name
    )

        with open(
            upload_path,
            "wb+"
        ) as destination:

            for chunk in pdf_file.chunks():

                destination.write(chunk)

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

        VectorStoreService.create_vector_store(
            chunks
        )

        return Response(
            {
                "message": "PDF uploaded successfully",
                "chunks": len(chunks)
            }
        )