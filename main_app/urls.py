from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('countries/', views.CountryList.as_view(), name='countries_index'),
    path('countries/<int:pk>/', views.CountryDetail.as_view(), name='countries_detail'),
    path('countries/<int:country_id>/add_comment/', views.add_comment, name='add_comment'),
    path('countries/<int:country_id>/delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('countries/<int:country_id>/update_comment/<int:comment_id>/', views.update_comment, name='update_comment'),
    path('countries/<int:country_id>/assoc_country/', views.assoc_country, name='assoc_country'),
    path('countries/<int:country_id>/unassoc_country/', views.unassoc_country, name='unassoc_country'),
    path('countries/<int:pk>/provinces/', views.ProvinceList.as_view(), name='provinces_index'),
    path('provinces/<int:pk>/counties', views.CountyList.as_view(), name='counties_index'),
    path('profiles/', views.ProfileList.as_view(), name='profiles_index'),
    path('profiles/<int:user_id>/', views.profiles_detail, name='profiles_detail'),
]
