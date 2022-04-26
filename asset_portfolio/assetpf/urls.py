from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('register/',views.register_attempt,name='register.attempt'),
    path('login/',views.login_attempt,name='login.attempt'),
    path('token/',views.token_send,name='token.send'),
    path('sucess/',views.sucess,name='sucess'),
    path('verify/<auth_token>',views.verify,name='verify'),
    path('error/',views.error,name='error'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('personalinfo/',views.personal_info,name='personal_info'),
    path('new/',views.new,name='new'),

    path('portfolio/',views.addshowPortfolio,name='addshowPortfolio'),
    
    path('delete/<int:id>/',views.deletePortfolio,name='delete_portfolio'),
    path('update/<int:id>/',views.updatePortfolio,name='update_portfolio'),
    
    
    
    
   
    

]
