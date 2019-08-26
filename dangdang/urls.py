from django.urls import path

from dangdang import views

app_name='dangdang'
urlpatterns = [
    path('index/', views.index,name='index'),
    path('lok_booklist/', views.booklist,name='booklist'),
    path('login/', views.login,name='login'),
    path('regist/', views.regist,name='regist'),
    path('registlogic/', views.regist_logic,name='registlogic'),
    path('registOk/', views.regist_ok,name='registOk'),
    path('login_logic/', views.login_logic,name='loginlogic'),
    path('getcaptcha/', views.getcaptcha,name='getcaptcha'),
    path('ajaxCode/', views.ajax_code,name='ajaxCode'),
    path('ajaxName/', views.ajax_name,name='ajaxName'),
    path('ajaxOut/', views.ajaxOut,name='ajaxOut'),
    # path('ajaxEmail/', views.ajaxEmail,name='ajaxEmail'),
]
