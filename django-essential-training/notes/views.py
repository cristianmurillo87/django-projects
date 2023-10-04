from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.http import Http404
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.views.generic.edit import DeleteView

from .forms import NotesForm
from .models import Note


class NotesListView(LoginRequiredMixin, ListView):
    model = Note
    template_name = "notes/notes_list.html"
    # in the view notes is used as the iterator
    context_object_name = "notes"
    login_url = "/login"

    def get_queryset(self):
        return self.request.user.notes.all()


class NotesDetailView(DetailView):
    model = Note
    context_object_name = "note"
    template_name = "notes/notes_detail.html"


class NotesCreateView(LoginRequiredMixin, CreateView):
    model = Note
    form_class = NotesForm
    success_url = "/smart/notes"
    template_name = "notes/notes_form.html"
    login_url = "/login"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class NotesUpdateView(UpdateView):
    model = Note
    form_class = NotesForm
    success_url = "/smart/notes"
    template_name = "notes/notes_form.html"


class NotesDeleteView(DeleteView):
    model = Note
    success_url = "/smart/notes"
    template_name = "notes/notes_delete.html"
