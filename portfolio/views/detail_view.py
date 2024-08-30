from django.views.generic import DetailView

from ..models import Project

# Create your views here.


class ProjectDetailView(DetailView):
    model = Project
    context_object_name = 'project'
    template_name = 'portfolio/pages/project_detail.html'

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context.update(
            {'is_detail_page': True}
        )
        return context

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        qs.filter(is_published=True)
        return qs
