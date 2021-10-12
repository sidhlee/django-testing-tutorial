# django-testing-tutorial

## Testing Layout with Django and Pytest

You can have tests folder inside each app where you have test files that correspond to the files that you're testing.

```text
budget/
  forms.py
  models.py
  urls.py
  views.py
  tests/
    __init__.py
    test_forms.py
    test_models.py
    test_urls.py
    test_views.py
```

Pytest requires `__init__.py` file in order to find the test packages.
