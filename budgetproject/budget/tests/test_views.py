from django.test import TestCase, Client
from django.urls import reverse
from budget.models import Project, Category, Expense
import json


class TestViews(TestCase):
    # We can set up necessary test attributes here.
    def setUp(self):
        self.client = Client()
        self.list_url = reverse("list")
        self.detail_url = reverse("detail", kwargs={"project_slug": "test-project"})
        # We need to create the project before making GET request at detail.
        self.test_project: Project = Project.objects.create(
            name="test-project", budget=95000
        )

    def test_project_list_GET(self):

        # Test
        response = self.client.get(self.list_url)

        # Assertion
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "budget/project-list.html")

    def test_project_detail_GET(self):
        # This will look for the project by the project slug.
        # We created a project passing in the name value which gets slugified into a slug
        response = self.client.get(self.detail_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "budget/project-detail.html")

    # Testing POST request
    def test_project_detail_POST_adds_new_expense(self):

        Category.objects.create(project=self.test_project, name="test_category")

        # Add new expense to the project
        response = self.client.post(
            # The url, 'test-project/' gets passed to the project_detail view function
            # and the captured value: 'test-project' is used to query the project from the database.
            self.detail_url,
            # This dict is used as the form data and passed along with the queried project
            # to create an expanse model instance.
            {
                "title": "test_expense",
                "amount": 1200,
                "category": "test_category",
            },
        )
        # At the end of project_detail view function, it returns redirect(project)
        # unless it returns early with other response.
        self.assertEquals(
            response.status_code, 302
        )  # assert 302 for successful redirection

        # Test that the expense was added
        # Renamed related model, Expense from the default "expense_set" to "expenses"
        # with related_name kwarg passed to ForeignKey in Expense
        self.assertEquals(self.test_project.expenses.first().title, "test_expense")

    # Test POST request with no data
    def test_project_detail_POST_no_data(self):
        response = self.client.post(self.detail_url, {})

        self.assertEquals(response.status_code, 302)
        # TestCase rollsback database to the initial state after each test
        self.assertEquals(self.test_project.expenses.count(), 0)

    def test_project_detail_DELETE_deletes_detail(self):
        # setUp runs before every test and database gets rolled back after each
        category = Category.objects.create(
            project=self.test_project, name="test_category"
        )
        Expense.objects.create(
            project=self.test_project,
            title="test_expense",
            amount=800,
            category=category,
        )

        response = self.client.delete(
            path=self.detail_url, content_type="application/json", data={"id": 1}
        )

        self.assertEquals(response.status_code, 204)
        self.assertEquals(self.test_project.expenses.count(), 0)

    def test_project_detail_DELETE_no_id(self):
        category = Category.objects.create(
            project=self.test_project, name="test_category"
        )
        Expense.objects.create(
            project=self.test_project,
            title="test_expense",
            amount=800,
            category=category,
        )

        response = self.client.delete(path=self.detail_url)

        self.assertEquals(response.status_code, 404)
        self.assertEquals(self.test_project.expenses.count(), 1)

    def test_project_create_POST(self):
        url = reverse("add")

        response = self.client.post(
            url,
            {
                # Should use different name from the one used in self.test_object in setUp()
                # Because Project slugifies from the name which is used in direction
                "name": "another-test-project",
                "budget": 1500,
                "categoriesString": "design,development",
            },
        )

        another_project = Project.objects.get(id=2)
        self.assertEquals(another_project.name, "another-test-project")
        first_category = Category.objects.get(id=1)
        second_category = Category.objects.get(id=2)
        self.assertEquals(first_category.project, another_project)
        self.assertEquals(first_category.name, "design")
        self.assertEquals(second_category.project, another_project)
        self.assertEquals(second_category.name, "development")
