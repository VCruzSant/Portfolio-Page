from django.shortcuts import render
from django.views.generic import ListView

from ..models import Project

# Create your views here.


def home(request):
    return render(request, 'portfolio/pages/home.html')


class RecipeListView(ListView):
    model = Project
    context_object_name = 'project'
    ordering = ['-id']
    template_name = 'portfolio/pages/home.html'
