from django.test import SimpleTestCase
from django.urls import reverse, resolve
from budget.views import project_list, ProjectCreateView, project_detail


# use SimpleTestCase when you don't need access database
class TestUrls(SimpleTestCase):
    def test_list_url_iresolves(self):
        # Get url from the name of the route
        # bound with url and route handler with django.urls.path
        url = reverse("list")
        # From url, get ResolveMatch that contains
        # ResolverMatch(func=budget.views.project_list, args=(), kwargs={}, url_name=list, app_names=[], namespaces=[])
        print("\n")
        print(f"resolve(list_url) -> {resolve(url)}")
        self.assertEquals(resolve(url).func, project_list)

    def test_add_url_resolves(self):
        # add route has class-based view, ProjectCreateView
        url = reverse("add")
        print("\n")
        # Class-based view's ResolvedMatch contains func points to the view class
        match = resolve(url)
        print(f"resolve(add_url) -> {match}")
        # match.func has the type of <class 'function'>
        print(f"type(match.func): {type(match.func)}")
        # match.func.view_class has the type of <class 'type'>
        print(f"type(match.func.view_class): {type(match.func.view_class)}")
        print(f"Add ResolverMatch.func: {resolve(url).func.__dict__}")

        # To compare resolves class with the view class, we need to access func.view_class
        self.assertEquals(resolve(url).func.view_class, ProjectCreateView)

    def test_detail_url_resolves(self):
        # detail route requites captures slug so we need to provide it in order to reverse it.
        url = reverse("detail", args=["some-slug"])
        print("\n")
        # Get the matching view function
        print(resolve(url).__dict__)
        self.assertEquals(resolve(url).func, project_detail)
