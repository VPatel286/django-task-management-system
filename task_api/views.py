from django.db.migrations import serializer
from django.tasks import task
from rest_framework import generics, status
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .models import Task, Tag, Category
from rest_framework.filters import SearchFilter, OrderingFilter
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db import transaction
from .serializers import (
    TaskSerializer,
    CategorySerializer,
    TagSerializer,
    RegisterSerializer,
    UserSerializer,
    ChangePasswordSerializer,
)
from .tasks import process_task
from .services import TaskService
from .permissions import IsTaskOwner


class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.none()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_fields = [
        "completed",
        "status",
    ]
    search_fields = ["title", "description"]

    ordering_fields = ["created_at", "updated_at", "title"]
    ordering = ["-created_at"]

    @extend_schema(
        responses=TaskSerializer,
        parameters=[
            OpenApiParameter(
                name="completed",
                type=OpenApiTypes.BOOL,
                location=OpenApiParameter.QUERY,
                description="Filter tasks by completion status.",
            ),
            OpenApiParameter(
                name="status",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Filter tasks by status.",
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return (
            Task.objects
            .filter(owner=self.request.user)
            .select_related("category")
            .prefetch_related("tags")
        )

    def perform_create(self, serializer):
        task = TaskService.create_task(
            validated_data=serializer.validated_data,
            owner=self.request.user,
        )
        serializer.instance = task

        transaction.on_commit(
            lambda: process_task.delay(task.id)
        )


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [
        IsAuthenticated,
        IsTaskOwner,
    ]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Task.objects.none()

        return (
            Task.objects
            .select_related("category")
            .prefetch_related("tags")
        )

    def perform_update(self, serializer):
        task = TaskService.update_task(
            task=serializer.instance,
            validated_data=serializer.validated_data,
        )

        serializer.instance = task

    def perform_destroy(self, instance):
        TaskService.delete_task(task=instance)


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class MeView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    throttle_classes = [
        AnonRateThrottle,
        UserRateThrottle,
    ]

    def get_object(self):
        return self.request.user


class ChangePasswordView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return Response(
            {"detail": "Password changed successfully."},
            status=status.HTTP_200_OK
        )


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]


class TagListCreateView(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]


class TagDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]
