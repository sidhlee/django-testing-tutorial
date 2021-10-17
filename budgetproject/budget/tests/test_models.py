from django.test import TestCase
from budget.models import Project, Expense, Category


class TestModels(TestCase):
    def setUp(self):
        self.project1 = Project.objects.create(name="project one", budget=10000)

    def test_project_is_assigned_slug_on_creation(self):
        self.assertEquals(self.project1.slug, "project-one")

    def test_budget_left(self):
        category = Category.objects.create(
            project=self.project1, name="design/development"
        )
        expense = Expense.objects.create(
            project=self.project1,
            title="initial design",
            amount=1500,
            category=category,
        )
        expense_two = Expense.objects.create(
            project=self.project1,
            title="frontend development",
            amount=4000,
            category=category,
        )

        self.assertEquals(self.project1.budget_left, 4500)

    def test_project_total_transactions(self):
        category = Category.objects.create(
            project=self.project1, name="design/development"
        )
        expense = Expense.objects.create(
            project=self.project1,
            title="initial design",
            amount=1500,
            category=category,
        )

        #  Ensure tranactions are taken from the correct subject
        another_project = Project.objects.create(name="another project", budget=500)
        expense2 = Expense.objects.create(
            project=another_project, title="expense2", amount=500, category=category
        )

        self.assertEquals(self.project1.total_transactions, 1)
