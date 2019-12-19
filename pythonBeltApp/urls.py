from django.urls import path
from . import views

urlpatterns = [
    path('main',views.index),
    path('createuser',views.createuser),
    path('login',views.login),
    path('travels',views.dashboard),
    path('logout',views.logout),
    path('travels/add',views.addtrip),
    path('createtrip',views.createtrip),
    path('jointrip/<tripsID>',views.jointrip),
    path('destination/<destination_Id>', views.destinationInfo),
    
]
