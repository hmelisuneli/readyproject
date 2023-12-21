from django.core.mail import send_mail
from django.forms import model_to_dict
from django.template.loader import render_to_string
from rest_framework import generics, viewsets
from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, FormView
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden, HttpResponseBadRequest, \
    HttpResponseServerError, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .form import *
from .models import *
from .permissions import IsAdminOrReadOnly
from .serializers import SupportSerializer
from .utils import *


class SupportAPIListPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 5


class SupportViewSet(viewsets.ModelViewSet):
    serializer_class = SupportSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def get_queryset(self):
        pk = self.kwargs.get("pk")

        if not pk:
            return Support.objects.all()

        return Support.objects.filter(pk=pk)

    @action(methods=['get'], detail=True)
    def categorydetail(self, request, pk=None):
        cats = Category.objects.get(pk=pk)
        return Response({'cats': cats.name})

    @action(methods=['get'], detail=False)
    def category(self, request):
        cats = Category.objects.all()
        return Response({'cats': [c.name for c in cats]})


class SupportAPIList(generics.ListCreateAPIView):
    queryset = Support.objects.all()
    serializer_class = SupportSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = SupportAPIListPagination


class SupportAPIDetailView(generics.RetrieveUpdateAPIView):
    queryset = Support.objects.all()
    serializer_class = SupportSerializer
    permission_classes = (IsAuthenticated,)


class SupportAPIDestroy(generics.RetrieveDestroyAPIView):
    queryset = Support.objects.all()
    serializer_class = SupportSerializer


class SupportHome(LoginRequiredMixin, DataMixin, ListView):
    model = Support
    template_name = 'support/home.html'
    context_object_name = 'posts'
    permission_required = ('admin')

    def get_queryset(self):
        return Support.objects.filter(is_published=True).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Main page")
        return dict(list(context.items()) + list(c_def.items()))


class AboutUs(DataMixin, ListView):
    model = Support
    template_name = 'support/aboutUs.html'

    def get_queryset(self):
        return Support.objects.filter(is_published=True).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        c_def = self.get_user_context(title="About Us")
        return ({
            'menu': menu,
            'title': 'About us Page',
        })


def news(request):
    return render(request, 'support/news.html', {'menu': menu, 'title': 'News'})


class AddPage(PermissionRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'support/addpage.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True
    permission_required = 'superuser'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Add page")
        return dict(list(context.items()) + list(c_def.items()))


class ShowPost(LoginRequiredMixin, DataMixin, DetailView):
    model = Support
    template_name = 'support/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'
    permission_required = ('admin')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'], cat_selected=context['post'].cat_id)
        return dict(list(context.items()) + list(c_def.items()))


class SupportCategory(LoginRequiredMixin, DataMixin, ListView):
    paginate_by = 2
    model = Support
    template_name = 'support/home.html'
    context_object_name = 'posts'
    permission_required = ('admin')
    allow_empty = False

    def get_queryset(self):
        return Support.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Category - ' + str(c.name),
                                      cat_selected=c.pk)
        return dict(list(context.items()) + list(c_def.items()))


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'support/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Register")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'support/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Authorization")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')


def sendEmail(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            content = form.cleaned_data['content']

            html = render_to_string('support/contactform.html', {
                'name': name,
                'email': email,
                'content': content
            })

            send_mail('The contact form subject', 'This is the message', 'noreply@codewithstein.com',
                      ['wingeddemon2274@gmail.com'], html_message=html)

            return redirect('contact')
    else:
        form = ContactForm()

    return render(request, 'support/contact.html', {
        'form': form,
        'menu': menu,
        'title': 'Contacts',
    })


# class ContactFormView(DataMixin, FormView):
#     form_class = ContactForm
#     template_name = 'support/contact.html'
#     success_url = reverse_lazy('home')
#
# def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         c_def = self.get_user_context(title="Contacts")
#         return dict(list(context.items()) + list(c_def.items()))
#
#     def form_valid(self, form):
#         print(form.cleaned_data)
#         return redirect('home')
#


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


def Forbidden(request, exception):
    return HttpResponseForbidden('<h1>Доступ запрещен </h1>')


def BadRequest(request, exception):
    return HttpResponseBadRequest('<h1>Не правильный запрос </h1>')


def ServerError(request):
    return HttpResponseServerError('<h1>Ошибка сервера </h1>')

# class SupportAPIView(APIView):
#     def get(self, request):
#
#         s = Support.objects.all()
#         return Response({'posts': SupportSerializer(s, many=True).data})
#
#     def post(self, request):
#         serializer = SupportSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#
#         return Response({'post': serializer.data})
#
#
#     def put(self, request, *args, **kwargs):
#         pk = kwargs.get("pk", None)
#         if not pk:
#             return Response({"error": "Method PUT not allowed"})
#
#         try:
#             instance = Support.objects.get(pk=pk)
#         except:
#             return Response({"error": "Object does not exists"})
#
#         serializer = SupportSerializer(data=request.data, instance=instance)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({"post": serializer.data})
#
#     def delete(self, request, *args, **kwargs):
#         pk = kwargs.get("pk", None)
#         if not pk:
#             return Response({"error": "Method DELETE not allowed"})
#
#
#         try:
#             instance = Support.objects.get(pk=pk)
#         except:
#             return Response({"error": "Object does not exists"})
#         instance.delete()
#
#
#         return Response({"post": "delete post " + str(pk)})
#
#


# class SupportAPIView(generics.ListAPIView):
#     queryset = Support.objects.all()
#     serializer_class = SupportSerializer
#


# def index(request):
#
#     context = {
#         'menu': menu,
#         'title': 'Main page',
#         'cat_selected': 0,
#
#     }
#
#     return render(request, 'support/home.html', context=context)


# def show_category(request, cat_id):
#
#
#     context = {
#         'menu': menu,
#         'title': 'Show categories',
#         'cat_selected': cat_id,
#     }
#
#     return render(request, 'support/home.html', context=context)

# def show_post(request, post_slug):
#     post = get_object_or_404(Support, slug=post_slug)
#
#     context = {
#         'post': post,
#         'menu': menu,
#         'title': post.title,
#         'cat_selected': post.cat_id,
#     }
#
#     return render(request, 'support/post.html', context=context)

# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
#     return render(request, 'support/addpage.html', {'form': form, 'menu': menu, 'title': 'Add page'})

