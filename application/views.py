from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from .models import Category, Note

from django.core.paginator import Paginator

from django.db.models import Q

# Create your views here.


class LoginViewNew(LoginView):
    template_name = 'application/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('notes')


class SignUpPage(FormView):
    template_name = 'application/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('notes')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(SignUpPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('notes')
        return super(SignUpPage, self).get(*args, **kwargs)


class NoteList(LoginRequiredMixin, ListView):
    model = Note
    context_object_name = 'notes'
    categories = Category.objects.all()
    context = {'categories': categories}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notes'] = context['notes'].filter(user=self.request.user)
        context['count'] = context['notes'].filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['notes'] = context['notes'].filter(Q(Q(title__icontains=search_input) |
                                                         Q(description__icontains=search_input)))

        context['search_input'] = search_input

        return context


class NoteDetail(LoginRequiredMixin, DetailView):
    model = Note
    context_object_name = 'note'


class NoteCreate(LoginRequiredMixin, CreateView):
    model = Note
    fields = ['title', 'description', 'image', 'category']
    success_url = reverse_lazy('notes')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(NoteCreate, self).form_valid(form)


class CategoryCreate(LoginRequiredMixin, CreateView):
    model = Category
    template_name = 'application/category_create.html'
    fields = '__all__'
    success_url = reverse_lazy('notes')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CategoryCreate, self).form_valid(form)


class NoteUpdate(LoginRequiredMixin, UpdateView):
    model = Note
    fields = ['title', 'description', 'image', 'category']
    success_url = reverse_lazy('notes')


class NoteDeleteView(LoginRequiredMixin, DeleteView):
    model = Note
    context_object_name = 'note'
    success_url = reverse_lazy('notes')


@login_required()
def CategoryViewList(request):
    cat = Category.objects.order_by('-id')

    paginator = Paginator(cat, 10)
    page = request.GET.get('page')
    categories = paginator.get_page(page)

    context = {'categories': cat}

    return render(request, 'application/category.html', context)


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    context_object_name = 'note'
    success_url = reverse_lazy('notes')


class CategoryUpdate(LoginRequiredMixin, UpdateView):
    model = Category
    fields = ['name']
    success_url = reverse_lazy('category')




