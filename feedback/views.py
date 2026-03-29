from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView, ListView, UpdateView

from .forms import FeedbackForm, FeedbackStatusForm
from .models import FeedbackEntry


class FeedbackCreateView(FormView):
    form_class = FeedbackForm
    template_name = "feedback/form.html"
    success_url = reverse_lazy("feedback:index")

    def form_valid(self, form):
        entry = form.save(commit=False)
        if self.request.user.is_authenticated:
            entry.created_by = self.request.user
        entry.save()
        messages.success(self.request, "反馈已提交，我们会尽快处理。")
        if self.request.headers.get("HX-Request") == "true":
            return HttpResponse('<div class="alert alert-success soft-alert mb-0">反馈已提交，我们会尽快处理。</div>')
        return super().form_valid(form)


class FeedbackListView(LoginRequiredMixin, ListView):
    model = FeedbackEntry
    context_object_name = "feedback_entries"
    template_name = "feedback/index.html"
    paginate_by = 12

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return FeedbackEntry.objects.all()
        return FeedbackEntry.objects.filter(created_by=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feedback_form"] = FeedbackForm()
        return context


class FeedbackDetailView(LoginRequiredMixin, DetailView):
    model = FeedbackEntry
    context_object_name = "feedback_entry"
    template_name = "feedback/detail.html"

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return FeedbackEntry.objects.all()
        return FeedbackEntry.objects.filter(created_by=user)


class FeedbackStatusUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = FeedbackEntry
    form_class = FeedbackStatusForm
    template_name = "feedback/status_edit.html"
    success_url = reverse_lazy("feedback:index")

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        messages.success(self.request, "反馈状态已更新。")
        return super().form_valid(form)
