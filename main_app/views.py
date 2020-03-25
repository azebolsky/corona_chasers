from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView
from .forms import RegistrationForm, CommentForm, AvatarForm
from .models import Global, Country, Province, Comment, Profile
from .utils import delete_file


def home(request):
    world = Global.objects.first()
    return render(request, 'home.html', {'world': world})


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid sign up - try again'
    form = RegistrationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)


@login_required
def add_comment(request, country_id):
    form = CommentForm(request.POST)
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.posted_at = datetime.now()
        new_comment.created_by = request.user
        new_comment.country_id = country_id
        new_comment.save()
    return redirect('countries_detail', pk=country_id)


@login_required
def delete_comment(request, country_id, comment_id):
    comment = Comment.objects.get(id=comment_id)
    if request.user.id == comment.created_by.id:
        comment.delete()
    return redirect('countries_detail', pk=country_id)


@login_required
def update_comment(request, country_id, comment_id):
    comment = Comment.objects.get(id=comment_id)
    if request.user.id == comment.created_by.id:
        comment.content = request.POST.get('content')
        comment.save()
    return redirect('countries_detail', pk=country_id)


def profiles_detail(request, user_id):
    user = User.objects.get(id=user_id)
    avatar_form = AvatarForm()
    return render(request, 'main_app/profile_detail.html', {'profile_user': user, 'avatar_form': avatar_form})


@login_required
def update_avatar(request):
    form = AvatarForm(request.POST, request.FILES)
    if form.is_valid():
        profile = Profile.objects.get(user_id=request.user.id)
        if profile.avatar:
            delete_file(profile.avatar)
        profile.avatar = form.save()
        profile.save()
    return redirect('profiles_detail', user_id=request.user.id)


@login_required
def assoc_country(request, country_id):
    country = Country.objects.get(id=country_id)
    country.users.add(request.user.id)
    return redirect('countries_detail', pk=country_id)


@login_required
def unassoc_country(request, country_id):
    country = Country.objects.get(id=country_id)
    country.users.remove(request.user.id)
    return redirect(request.META.get('HTTP_REFERER'))


class ProfileList(ListView):
    model = User
    template_name = 'main_app/profile_list.html'

    def get_queryset(self):
        query = self.request.GET.get('search')
        if query:
            return User.objects.filter(username__icontains=query).order_by('username')
        return User.objects.all().order_by('username')


class CountryList(ListView):
    model = Country
    sort_type = 'ascend'

    def get_queryset(self):
        search_query = self.request.GET.get('search')
        sort_query = self.request.GET.get('sort')
        order_query = self.request.GET.get('order_by')
        if search_query:
            return Country.objects.filter(name__icontains=search_query)
        if sort_query == 'ascend':
            self.sort_type = 'descend'
            return Country.objects.all().order_by(order_query)
        if sort_query == 'descend':
            self.sort_type = 'ascend'
            return Country.objects.all().order_by(f'-{order_query}')
        return Country.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sort_type'] = self.sort_type
        return context


class CountryDetail(DetailView):
    model = Country

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context


class ProvinceList(ListView):
    sort_type = 'ascend'

    def get_queryset(self):
        search_query = self.request.GET.get('search')
        sort_query = self.request.GET.get('sort')
        order_query = self.request.GET.get('order_by')
        if search_query:
            return Province.objects.filter(country=self.kwargs['pk'], name__icontains=search_query)
        if sort_query == 'ascend':
            self.sort_type = 'descend'
            return Province.objects.filter(country=self.kwargs['pk']).order_by(order_query)
        if sort_query == 'descend':
            self.sort_type = 'ascend'
            return Province.objects.filter(country=self.kwargs['pk']).order_by(f'-{order_query}')
        return Province.objects.filter(country=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sort_type'] = self.sort_type
        return context
