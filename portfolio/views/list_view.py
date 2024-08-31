from django.views.generic import ListView

from ..models import Project, Portfolio

# Create your views here.


class ProjectListView(ListView):
    model = Project
    context_object_name = 'projects'
    ordering = ['-id']
    template_name = 'portfolio/pages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['portfolio_images'] = Portfolio.objects.all()
        return context
