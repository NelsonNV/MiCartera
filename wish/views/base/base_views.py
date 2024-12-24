from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.urls import reverse_lazy


class BaseListView(ListView):
    template_name = "wish/base_list.html"
    context_object_name = "objects"
    table_headers = []
    table_fields = []
    update_url_name = None
    delete_url_name = None
    create_url_name = None
    has_permission = True
    null_values = None
    model_name_plural = "tabla"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["table_headers"] = self.table_headers
        context["table_fields"] = self.table_fields
        context["update_url_name"] = self.update_url_name
        context["delete_url_name"] = self.delete_url_name
        context["create_url_name"] = self.create_url_name
        context["has_permission"] = self.has_permission
        context["null_values"] = self.null_values
        context["model_name_plural"] = self.model_name_plural
        return context


class BaseDetailView(DetailView):
    template_name = "base_detail.html"
    context_object_name = "object"


class BaseCreateView(CreateView):
    template_name = "wish/base_form.html"
    success_url = reverse_lazy("home")


class BaseUpdateView(UpdateView):
    template_name = "wish/base_form.html"
    success_url = reverse_lazy("home")


class BaseDeleteView(DeleteView):
    template_name = "wish/base_confirm_delete.html"
    success_url = reverse_lazy("home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["list_view_name"] = getattr(self, "list_url_name", None)
        return context
