from django.urls import path
from .views import (
    TaskListCreateView,
    TaskDetailView,
    CategoryListCreateView,
    CategoryDetailView,
    TagListCreateView,
    TagDetailView,
    RegisterView,
    MeView,
    ChangePasswordView,
)

urlpatterns = [
    path("tasks/", TaskListCreateView.as_view(), name="task-list-create"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("register/", RegisterView.as_view(), name="register"),
    path("me/", MeView.as_view(), name="me"),
    path(
        "change-password/",
        ChangePasswordView.as_view(),
        name="change-password",
    ),
    path("categories/",
         CategoryListCreateView.as_view(),
         name="category-list-create"),
    path(
        "categories/<int:pk>/",
        CategoryDetailView.as_view(),
        name="category-detail",
    ),
    path(
        "tags/",
        TagListCreateView.as_view(),
        name="tag-list-create",
    ),
    path(
        "tags/<int:pk>/",
        TagDetailView.as_view(),
        name="tag-detail",
    ),
]
