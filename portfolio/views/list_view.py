from django.views.generic import ListView

from ..models import Project

# Create your views here.


class ProjectListView(ListView):
    model = Project
    context_object_name = 'projects'
    ordering = ['-id']
    template_name = 'portfolio/pages/home.html'
