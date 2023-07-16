from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from .forms import AddItemForm, RegisterUserForm, LoginUserForm
from .models import *

menu = [{'title': "Домашняя страница", 'url_name': 'home'},
        {'title': "Добавить товар", 'url_name': 'add_item'},
        {'title': "Корзина", 'url_name': 'shopping_cart'}
]
class Home(ListView):
    paginate_by = 5
    model = Items
    template_name = 'index.html'
    context_object_name = 'items'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Pet shop'
        context['category_list'] = Category.objects.all()
        context['category_selected'] = 0
        return context

    def get_queryset(self):
        return Items.objects.filter(is_published=True)

class AddItem(CreateView):
    form_class = AddItemForm
    template_name = 'additem.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление товара'
        context['category_list'] = Category.objects.all()
        context['menu'] = menu
        return context

def show_item(request, item_id):
    item = get_object_or_404(Items, id=item_id)

    context = {
        'item': item,
        'menu': menu,
        'title': item.name,
        'category_list': Category.objects.all(),
        'category_selected': item.category_id,
    }

    return render(request, 'item.html', context=context)

def show_category(request, category_id):
    items = Items.objects.filter(category_id=category_id)

    if len(items) == 0:
        raise Http404()

    context = {
        'items': items,
        'menu': menu,
        'category_list': Category.objects.all(),
        'title': Category.objects.filter(id=category_id)[0],
        'category_selected': category_id,
    }

    return render(request, 'index.html', context=context)

def add_item_to_shopping_cart (request):
    item_id = request.GET.get('item_id')

    Reviews.objects.create(id_item_id=item_id, id_user_id=request.user.id)

    return redirect('home')

def show_shopping_cart(request):
    user_id = request.user.id
    items1 = Reviews.objects.filter(id_user_id=user_id)
    item_id = items1.values_list('id_item_id', flat=True)
    items = Items.objects.filter(id__in=item_id)

    context = {
        'items': items,
        'menu': menu,
        'category_list': Category.objects.all(),
        'title': "Корзина",
    }

    return render(request, 'shopping_cart.html', context=context)

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['category_list'] = Category.objects.all()
        context['category_selected'] = 0
        context['title'] = 'Регистрация'
        return dict(list(context.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['category_list'] = Category.objects.all()
        context['category_selected'] = 0
        context['title'] = 'Авторизация'
        return dict(list(context.items()))

    def get_success_url(self):
        return reverse_lazy('home')

def logout_user(request):
    logout(request)
    return redirect('home')