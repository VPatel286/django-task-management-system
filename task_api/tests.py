from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from django.test import override_settings
from .models import Task
from rest_framework.settings import api_settings
from django.core.cache import cache
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from unittest.mock import patch


class CustomUserThrottle(UserRateThrottle):
    scope = "test_user"


User = get_user_model()


class TaskAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="TestPassword123!"
        )

        self.other_user = User.objects.create_user(
            username="otheruser",
            password="TestPassword123!"
        )

        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )

        self.task = Task.objects.create(
            title="Test Task",
            description="Testing API",
            completed=False,
            owner=self.user,
        )

        self.other_user_task = Task.objects.create(
            title="Other User Task",
            description="Belongs to another user",
            completed=False,
            owner=self.other_user,
        )

        self.completed_task = Task.objects.create(
            title="Completed Task",
            description="This task is completed",
            completed=True,
            owner=self.user,
        )

    def test_authenticated_user_can_list_tasks(self):
        response = self.client.get("/api/v1/tasks/")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["count"],
            2
        )

        self.assertEqual(
            response.data["results"][0]["title"],
            "Completed Task"
        )

    def test_filter_completed_tasks(self):
        response = self.client.get(
            "/api/v1/tasks/?completed=true"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["count"],
            1
        )

        self.assertTrue(
            response.data["results"][0]["completed"]
        )

    def test_filter_incomplete_tasks(self):
        response = self.client.get(
            "/api/v1/tasks/?completed=false"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["count"],
            1
        )

        self.assertFalse(
            response.data["results"][0]["completed"]
        )

    def test_unauthenticated_user_cannot_access_tasks(self):
        self.client.credentials()

        response = self.client.get(
            "/api/v1/tasks/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_user_can_create_task(self):
        data = {
            "title": "New Test Task",
            "description": "Created during automated testing",
            "completed": False,
        }

        response = self.client.post(
            "/api/v1/tasks/",
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response.data["owner"],
            self.user.id
        )

    def test_task_owner_cannot_be_changed(self):
        data = {
            "title": "Updated Task",
            "owner": self.other_user.id,
        }

        response = self.client.patch(
            f"/api/v1/tasks/{self.task.id}/",
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.task.refresh_from_db()

        self.assertEqual(
            self.task.owner,
            self.user
        )

    def test_user_cannot_access_another_users_task(self):
        other_task = Task.objects.create(
            title="Private Task",
            description="Should not be accessible",
            owner=self.other_user,
        )

        response = self.client.get(
            f"/api/v1/tasks/{other_task.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_user_can_update_own_task(self):
        data = {
            "completed": True
        }

        response = self.client.patch(
            f"/api/v1/tasks/{self.task.id}/",
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.task.refresh_from_db()

        self.assertTrue(
            self.task.completed
        )

    def test_user_can_delete_own_task(self):
        response = self.client.delete(
            f"/api/v1/tasks/{self.task.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertFalse(
            Task.objects.filter(
                id=self.task.id
            ).exists()
        )

    def test_search_tasks_by_title(self):
        response = self.client.get(
            "/api/v1/tasks/?search=Completed"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["count"],
            1
        )

        self.assertEqual(
            response.data["results"][0]["title"],
            "Completed Task"
        )

    def test_search_tasks_by_description(self):
        response = self.client.get(
            "/api/v1/tasks/?search=completed"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["count"],
            1
        )

        self.assertEqual(
            response.data["results"][0]["title"],
            "Completed Task"
        )

    def test_order_tasks_by_title_ascending(self):
        response = self.client.get(
            "/api/v1/tasks/?ordering=title"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["results"][0]["title"],
            "Completed Task"
        )

        self.assertEqual(
            response.data["results"][1]["title"],
            "Test Task"
        )

    def test_order_tasks_by_title_descending(self):
        response = self.client.get(
            "/api/v1/tasks/?ordering=-title"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["results"][0]["title"],
            "Test Task"
        )

        self.assertEqual(
            response.data["results"][1]["title"],
            "Completed Task"
        )

    def test_task_pagination(self):
        response = self.client.get(
            "/api/v1/tasks/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["count"],
            2
        )

        self.assertEqual(
            len(response.data["results"]),
            2
        )

        self.assertIsNone(
            response.data["previous"]
        )

        self.assertIsNone(
            response.data["next"]
        )

    def test_task_title_cannot_be_empty(self):
        data = {
            "title": "",
            "description": "Invalid task",
            "completed": False,
        }

        response = self.client.post(
            "/api/v1/tasks/",
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertIn(
            "title",
            response.data
        )

    def test_task_title_cannot_exceed_200_characters(self):
        data = {
            "title": "A" * 201,
            "description": "Invalid task",
            "completed": False,
        }

        response = self.client.post(
            "/api/v1/tasks/",
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertIn(
            "title",
            response.data
        )

    def test_user_cannot_update_another_users_task(self):
        other_task = Task.objects.create(
            title="Other User Task",
            description="Private task",
            completed=False,
            owner=self.other_user,
        )

        data = {
            "title": "Hacked Task",
            "completed": True,
        }

        response = self.client.patch(
            f"/api/v1/tasks/{other_task.id}/",
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

        other_task.refresh_from_db()

        self.assertEqual(
            other_task.title,
            "Other User Task"
        )

        self.assertFalse(
            other_task.completed
        )

    def test_user_cannot_delete_another_users_task(self):
        other_task = Task.objects.create(
            title="Other User Task",
            description="Private task",
            completed=False,
            owner=self.other_user,
        )

        response = self.client.delete(
            f"/api/v1/tasks/{other_task.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

        self.assertTrue(
            Task.objects.filter(
                id=other_task.id
            ).exists()
        )

    def test_user_can_register(self):
        data = {
            "username": "registereduser",
            "password": "SecurePassword123!",
        }

        response = self.client.post(
            "/api/v1/register/",
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response.data["username"],
            "registereduser"
        )

        self.assertNotIn(
            "password",
            response.data
        )

        self.assertTrue(
            User.objects.filter(
                username="registereduser"
            ).exists()
        )

    def test_registration_requires_password_of_at_least_8_characters(self):
        data = {
            "username": "shortpassworduser",
            "password": "1234567",
        }

        response = self.client.post(
            "/api/v1/register/",
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertIn(
            "password",
            response.data
        )

    def test_authenticated_user_can_access_me(self):
        response = self.client.get(
            "/api/v1/me/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["id"],
            self.user.id
        )

        self.assertEqual(
            response.data["username"],
            self.user.username
        )

        self.assertNotIn(
            "password",
            response.data
        )

    def test_unauthenticated_user_cannot_access_me(self):
        self.client.credentials()

        response = self.client.get(
            "/api/v1/me/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_registration_rejects_common_password(self):
        data = {
            "username": "commonpassworduser",
            "password": "password",
        }

        response = self.client.post(
            "/api/v1/register/",
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertIn(
            "password",
            response.data
        )

    def test_registration_rejects_password_similar_to_username(self):
        data = {
            "username": "johnsmith",
            "password": "johnsmith123",
        }

        response = self.client.post(
            "/api/v1/register/",
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertIn(
            "password",
            response.data
        )

    def test_user_can_change_password(self):
        data = {
            "old_password": "TestPassword123!",
            "new_password": "NewTestPassword456!",
        }

        response = self.client.post(
            "/api/v1/change-password/",
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["detail"],
            "Password changed successfully."
        )

        self.user.refresh_from_db()

        self.assertTrue(
            self.user.check_password(
                "NewTestPassword456!"
            )
        )

    def test_change_password_rejects_wrong_old_password(self):
        data = {
            "old_password": "WrongCurrentPassword123!",
            "new_password": "NewTestPassword456!",
        }

        response = self.client.post(
            "/api/v1/change-password/",
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertIn(
            "old_password",
            response.data
        )

    def test_change_password_rejects_weak_new_password(self):
        data = {
            "old_password": "TestPassword123!",
            "new_password": "1234567",
        }

        response = self.client.post(
            "/api/v1/change-password/",
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertIn(
            "new_password",
            response.data
        )

    def test_unauthenticated_user_cannot_change_password(self):
        self.client.credentials()

        data = {
            "old_password": "TestPassword123!",
            "new_password": "NewTestPassword456!",
        }

        response = self.client.post(
            "/api/v1/change-password/",
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_user_can_update_own_profile(self):
        data = {
            "username": "updateduser",
        }

        response = self.client.patch(
            "/api/v1/me/",
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["id"],
            self.user.id
        )

        self.assertEqual(
            response.data["username"],
            "updateduser"
        )

        self.user.refresh_from_db()

        self.assertEqual(
            self.user.username,
            "updateduser"
        )

    def test_user_cannot_update_profile_to_existing_username(self):
        data = {
            "username": self.other_user.username,
        }

        response = self.client.patch(
            "/api/v1/me/",
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertIn(
            "username",
            response.data
        )

    def test_user_id_cannot_be_changed(self):
        data = {
            "id": 999,
            "username": "safeupdateduser",
        }

        response = self.client.patch(
            "/api/v1/me/",
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["id"],
            self.user.id
        )

        self.assertEqual(
            response.data["username"],
            "safeupdateduser"
        )

        self.user.refresh_from_db()

        self.assertEqual(
            self.user.id,
            response.data["id"]
        )

    @override_settings(
        REST_FRAMEWORK={
            **settings.REST_FRAMEWORK,
            "DEFAULT_THROTTLE_RATES": {
                "anon": "20/minute",
                "user": "2/minute",
            },
        }
    )
    @patch.object(
        UserRateThrottle,
        "THROTTLE_RATES",
        {
            "user": "2/minute",
        }
    )
    def test_authenticated_user_is_throttled(self):
        cache.clear()

        response1 = self.client.get(
            "/api/v1/me/"
        )

        response2 = self.client.get(
            "/api/v1/me/"
        )

        response3 = self.client.get(
            "/api/v1/me/"
        )

        self.assertEqual(
            response1.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response2.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response3.status_code,
            status.HTTP_429_TOO_MANY_REQUESTS
        )

    @override_settings(
        REST_FRAMEWORK={
            **settings.REST_FRAMEWORK,
            "DEFAULT_THROTTLE_RATES": {
                "anon": "2/minute",
                "user": "100/minute",
            },
        }
    )
    @patch.object(
        AnonRateThrottle,
        "THROTTLE_RATES",
        {
            "anon": "2/minute",
        }
    )
    def test_anonymous_user_is_throttled(self):
        cache.clear()

        self.client.credentials()

        response1 = self.client.post(
            "/api/v1/register/",
            {
                "username": "anonymous_test_1",
                "password": "TestPassword123!",
            },
            format="json",
        )

        response2 = self.client.post(
            "/api/v1/register/",
            {
                "username": "anonymous_test_2",
                "password": "TestPassword123!",
            },
            format="json",
        )

        response3 = self.client.post(
            "/api/v1/register/",
            {
                "username": "anonymous_test_3",
                "password": "TestPassword123!",
            },
            format="json",
        )

        self.assertEqual(
            response1.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response2.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response3.status_code,
            status.HTTP_429_TOO_MANY_REQUESTS
        )

    def test_unauthenticated_user_cannot_create_task(self):
        self.client.credentials()

        data = {
            "title": "Unauthorized Task",
            "description": "Should not be created",
            "completed": False,
        }

        response = self.client.post(
            "/api/v1/tasks/",
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_user_cannot_access_another_users_task(self):
        response = self.client.get(
            f"/api/v1/tasks/{self.other_user_task.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_user_cannot_update_another_users_task(self):
        data = {
            "title": "Hacked Task",
        }

        response = self.client.patch(
            f"/api/v1/tasks/{self.other_user_task.id}/",
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_user_cannot_delete_another_users_task(self):
        response = self.client.delete(
            f"/api/v1/tasks/{self.other_user_task.id}/"
        )
        response = self.client.delete(
            f"/api/v1/tasks/{self.other_user_task.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_create_task_requires_title(self):
        data = {
            "description": "Task without a title",
            "completed": False,
        }

        response = self.client.post(
            "/api/v1/tasks/",
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_create_task_rejects_invalid_priority(self):
        data = {
            "title": "Invalid Priority Task",
            "description": "Testing invalid priority",
            "priority": "SUPER_HIGH",
        }

        response = self.client.post(
            "/api/v1/tasks/",
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_create_task_rejects_invalid_status(self):
        data = {
            "title": "Invalid Status Task",
            "description": "Testing invalid status",
            "status": "INVALID_STATUS",
        }

        response = self.client.post(
            "/api/v1/tasks/",
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    @patch("task_api.views.process_task.delay")
    def test_create_task_schedules_celery_task(self, mock_delay):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )

        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.post(
                "/api/v1/tasks/",
                {
                    "title": "Celery API Test",
                    "description": "Testing Celery scheduling",
                    "completed": False,
                    "priority": "HIGH",
                    "status": "TODO",
                    "tags": [],
                },
                format="json",
            )

        self.assertEqual(response.status_code, 201)

        task_id = response.data["id"]

        mock_delay.assert_called_once_with(task_id)
