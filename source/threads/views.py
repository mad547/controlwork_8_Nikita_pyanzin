from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator

from threads.forms import ThreadForm, AnswerForm, SearchForm
from threads.models import Thread, Answer


class IndexView(ListView):
    template_name = 'threads/index.html'
    context_object_name = 'threads'
    paginate_by = 10

    def get_queryset(self):
        queryset = Thread.objects.all().order_by('-created_at')
        query = self.request.GET.get('query', '')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = SearchForm(self.request.GET)
        context['query'] = self.request.GET.get('query', '')
        return context


class ThreadDetailView(DetailView):
    model = Thread
    template_name = 'threads/thread_detail.html'
    context_object_name = 'thread'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        answers = self.object.answers.order_by('created_at')
        paginator = Paginator(answers, 10)
        page_number = self.request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        context['answers'] = page_obj
        context['page_obj'] = page_obj
        context['is_paginated'] = page_obj.has_other_pages()
        context['answer_form'] = AnswerForm()
        return context


class ThreadCreateView(LoginRequiredMixin, CreateView):
    model = Thread
    template_name = 'threads/thread_form.html'
    form_class = ThreadForm

    def form_valid(self, form):
        thread = form.save(commit=False)
        thread.author = self.request.user
        thread.save()
        return redirect('threads:thread_detail', pk=thread.pk)


class ThreadUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Thread
    template_name = 'threads/thread_form.html'
    form_class = ThreadForm

    def test_func(self):
        thread = self.get_object()
        return self.request.user == thread.author or \
               self.request.user.has_perm('threads.change_thread')

    def get_success_url(self):
        return reverse_lazy('threads:thread_detail', kwargs={'pk': self.object.pk})


class ThreadDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Thread
    template_name = 'threads/thread_confirm_delete.html'
    context_object_name = 'thread'
    success_url = reverse_lazy('index')

    def test_func(self):
        thread = self.get_object()
        return self.request.user == thread.author or \
               self.request.user.has_perm('threads.delete_thread')


class AnswerCreateView(LoginRequiredMixin, CreateView):
    model = Answer
    form_class = AnswerForm

    def form_valid(self, form):
        thread = get_object_or_404(Thread, pk=self.kwargs.get('pk'))
        answer = form.save(commit=False)
        answer.author = self.request.user
        answer.thread = thread
        answer.save()
        thread.answers_count += 1
        thread.save()
        self.request.user.profile.messages_count += 1
        self.request.user.profile.save()
        return redirect('threads:thread_detail', pk=thread.pk)


class AnswerUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Answer
    template_name = 'threads/answer_form.html'
    form_class = AnswerForm

    def test_func(self):
        answer = self.get_object()
        return self.request.user == answer.author or \
               self.request.user.has_perm('threads.change_answer')

    def get_success_url(self):
        return reverse_lazy('threads:thread_detail', kwargs={'pk': self.object.thread.pk})


class AnswerDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Answer
    template_name = 'threads/answer_confirm_delete.html'
    context_object_name = 'answer'

    def test_func(self):
        answer = self.get_object()
        return self.request.user == answer.author or \
               self.request.user.has_perm('threads.delete_answer')

    def form_valid(self, form):
        answer = self.get_object()
        thread = answer.thread
        thread.answers_count -= 1
        thread.save()
        answer.author.profile.messages_count -= 1
        answer.author.profile.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('threads:thread_detail', kwargs={'pk': self.object.thread.pk})