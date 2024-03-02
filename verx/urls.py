from django.contrib import admin
from django.urls import path
from django.contrib.auth import views
from django.conf import settings
from django.conf.urls.static import static

from brain_ag.views import HomeView, ProdutorAdd, ProdutorView, ProdutorEdit, ProdutorDel


urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/login/', views.LoginView.as_view(redirect_authenticated_user='news/'), name='login'), #TODO: Remover
    path('', HomeView.as_view(), name='home'),
    path('produtor_add/', ProdutorAdd.as_view(), name='produtor-add'),
    path('produtores/', ProdutorView.as_view(), name='produtores'),
    path('produtor_edit/<int:pk>', ProdutorEdit.as_view(), name='produtor-edit'),
    path('produtor_del/<int:pk>', ProdutorDel.as_view(), name='produtor-del'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
