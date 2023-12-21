from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path
from django.views.decorators.cache import cache_page
from .views import *

urlpatterns = [
    # path('',cache_page(60)(SupportHome.as_view()),name='home'),
    # path('category/<slug:cat_slug>/',cache_page(60)(SupportCategory.as_view()),name='category'),
    path('home/', SupportHome.as_view(), name='home'),
    path('about/', AboutUs.as_view(), name='about'),
    path('news/', news, name='news'),
    path('addpage/', AddPage.as_view(), name='add_page'),
    # path('contact/', ContactFormView.as_view(), name='contact'),
    path('', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', SupportCategory.as_view(), name='category'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = pageNotFound
handler403 = Forbidden
handler400 = BadRequest
handler500 = ServerError
