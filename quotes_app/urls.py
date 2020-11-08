from django.urls import path     
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('quotes', views.displayQuotes),
    path('add_quote', views.addQuote),
    path('delete_quote/<int:quote_id>', views.deleteQuote),
    path('add_like/<int:quote_id>', views.addLike),
    path('user_page/<int:user_id>', views.displayUser),
    path('edit_user', views.getUserEditPage),
    path('update_user', views.updateUser)
]