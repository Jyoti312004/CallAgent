import traceback
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from typing import Dict, Any
from django.db import transaction
from src.knowledge_base.knowledge import KnowledgeBase
from src.model_helpers import KnowledgeBaseTypeOptions, QueryRequestStatusOptions, SourceOptions
from src.models import QueryRequest, User
from src.serializers import QueryRequestSerializer


class KnowledgeBaseViewSet(viewsets.ViewSet):
    """ViewSet for interacting with the Knowledge Base."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.knowledge_base = KnowledgeBase()

    @action(detail=False, methods=["get"], url_path="search-query")
    def search_query(self, request):
        """Search for similar entries in the knowledge base."""
        query = request.query_params.get("query", "")

        if not query:
            return Response(
                {"error": "Query parameter is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        similar_entries = self.knowledge_base._find_similar_entries(query)
        system_info = self.knowledge_base.get_system_information()

        response_data = {
            "similar_entries": similar_entries,
            "salon_information": system_info,
        }

        return Response(response_data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="add-knowledge")
    @transaction.atomic()
    def add_knowledge(self, request):
        """Add or update knowledge in the knowledge base."""
        try:
            data = request.data

            question = data.get("question", "")
            answer = data.get("answer", "")
            source = data.get("source", SourceOptions.SUPERVISOR)
            knowledge_type = data.get("type", KnowledgeBaseTypeOptions.QUERY)
            description = data.get("description", {})
            description_key = data.get("description_key", "info")
            query_request_id = data.get("query_request_id", None)

            if isinstance(knowledge_type, str):
                try:
                    knowledge_type = KnowledgeBaseTypeOptions[knowledge_type.upper()]
                except KeyError:
                    return Response(
                        {"error": f"Invalid knowledge type: {knowledge_type}"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            if isinstance(source, str):
                try:
                    source = SourceOptions[source]
                except KeyError:
                    return Response(
                        {"error": f"Invalid source: {source}"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            success, result = self.knowledge_base.add_or_update_knowledge(
                question=question,
                answer=answer,
                source=source,
                type=knowledge_type,
                description=description,
                description_key=description_key,
                query_request_id=query_request_id,
                **{
                    k: v
                    for k, v in data.items()
                    if k
                    not in [
                        "question",
                        "answer",
                        "source",
                        "type",
                        "description",
                        "description_key",
                        "query_request_id",
                    ]
                },
            )

            if success:
                return Response(
                    {"message": "Knowledge added/updated successfully", "id": result},
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response({"error": result}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("ERRROOROROROR",traceback.format_exc())
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class QueryRequestViewSet(viewsets.ModelViewSet):

    queryset = QueryRequest.objects.all()
    serializer_class = QueryRequestSerializer

    @action(detail=False, methods=["post"], url_path="create-query")
    def create_query(self, request):
        """Create a new query request."""
        try:
            data = request.data
            user_id = data.get("user_id")
            question = data.get("question")

            if not user_id or not question:
                return Response(
                    {"error": "User ID and question are required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            print("USER ID", user_id)
            user = User.objects.filter(id=user_id).first()
            print("USER", user)
            query_request = QueryRequest.objects.create(user=user, question=question)
            return Response(
                {"message": "Query request created successfully", "id": query_request.id},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            print(traceback.format_exc())
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=False, methods=["get"], url_path="get-query")
    def get_query(self, request):
        """Get a specific query request."""
        try:
            query_id = request.query_params.get("query_id")
            if not query_id:
                return Response(
                    {"error": "Query ID is required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            query_request = QueryRequest.objects.filter(id=query_id).first()
            if not query_request:
                return Response(
                    {"error": "Query request not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            serializer = self.get_serializer(query_request)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=False, methods=["get"], url_path="get-all-queries")
    def get_all_queries(self, request):
        """Get all query requests."""
        try:
            query_requests = QueryRequest.objects.all()
            serializer = self.get_serializer(query_requests, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
    @action(detail=False, methods=["get"], url_path="pending-query")
    def get_pending_queries(self, request):
        """Get all pending query requests."""
        try:
            pending_queries = QueryRequest.objects.filter(
                status=QueryRequestStatusOptions.PENDING
            )
            serializer = self.get_serializer(pending_queries, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=False, methods=["post"], url_path="resolve-query")
    def resolve_query(self, request):
        """Resolve a specific query request."""
        try:
            data = request.data
            query_id = data.get("query_id")
            if not query_id:
                return Response(
                    {"error": "Query ID is required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            query_request = QueryRequest.objects.filter(id=query_id).first()
            if not query_request:
                return Response(
                    {"error": "Query request not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            query_request.status = QueryRequestStatusOptions.RESOLVED
            query_request.save()
            return Response(
                {"message": "Query request resolved successfully"},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=False, methods=["delete"], url_path="delete-query")
    def delete_query(self, request):
        """Delete a specific query request."""
        try:
            query_id = request.query_params.get("query_id")
            if not query_id:
                return Response(
                    {"error": "Query ID is required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            query_request = QueryRequest.objects.filter(id=query_id).first()
            if not query_request:
                return Response(
                    {"error": "Query request not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            query_request.delete()
            return Response(
                {"message": "Query request deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
