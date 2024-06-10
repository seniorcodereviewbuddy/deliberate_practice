"""Module of all Django App code related to the admin page.

Any models that should appear on the admin page need
to be registered here.
"""

from django.contrib import admin

from .models import results, routine

admin.site.register(routine.Activity)
admin.site.register(results.PracticeSet)
