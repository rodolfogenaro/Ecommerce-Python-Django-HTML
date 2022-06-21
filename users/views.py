from django.views.generic import TemplateView

from .models import User

class AdminPageView(TemplateView):
    template_name = "admin.html"