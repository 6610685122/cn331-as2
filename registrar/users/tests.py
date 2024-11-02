from django.test import TestCase
import unittest
from .models import Course, QuotaRequest
from django.contrib.auth.models import User

# Create your tests here.
class CourseModelTest(TestCase):
    def setUp(self):
        # Create a course instance
        self.course = Course.objects.create(
            code="CN101",
            name="Intro to Computer Engineering",
            semester="2",
            academic_year=2024,
            seats=30
        )

    def test_course_str_method(self):
        # Test the __str__ method output
        self.assertEqual(str(self.course), "CN101 - Intro to Computer Engineering")

    def test_course_default_is_quota_open(self):
        # Test the default value of is_quota_open
        self.assertTrue(self.course.is_quota_open)

    def test_course_fields(self):
        # Verify field values for the created course
        self.assertEqual(self.course.code, "CN101")
        self.assertEqual(self.course.name, "Intro to Computer Engineering")
        self.assertEqual(self.course.semester, "2")
        self.assertEqual(self.course.academic_year, 2024)
        self.assertEqual(self.course.seats, 30)


class QuotaRequestModelTest(TestCase):
    def setUp(self):
        # Create a user and a course instance
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.course = Course.objects.create(
            code="CN101",
            name="Intro to Computer Engineering",
            semester="2",
            academic_year=2024,
            seats=30
        )
        # Create a QuotaRequest instance
        self.quota_request = QuotaRequest.objects.create(
            user=self.user,
            course=self.course
        )

    def test_quota_request_str_method(self):
        # Test the __str__ method output
        self.assertEqual(str(self.quota_request), "testuser - Intro to Computer Engineering")

    def test_quota_request_default_is_approved(self):
        # Test the default value of is_approved
        self.assertFalse(self.quota_request.is_approved)

    def test_quota_request_fields(self):
        # Verify field values for the created quota request
        self.assertEqual(self.quota_request.user, self.user)
        self.assertEqual(self.quota_request.course, self.course)