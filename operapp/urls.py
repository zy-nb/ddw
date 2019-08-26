from django.urls import path

from operapp import views
app_name='operapp'
urlpatterns = [
    path('cart/',views.cart,name='cart'),
    path('bookIntro/',views.book_intro,name='bookIntro'),
    path('addCart/',views.add_cart,name='addCart'),
    path('updateCart/',views.update_cart,name='updateCart'),
    path('delBook/',views.del_book,name='delBook'),
    path('cartSubmit/',views.cartSubmit,name='cartSubmit'),
    path('submitOK/',views.submitOK,name='submitOK'),
    path('cartSubmitOK/',views.cartSubmitOK,name='cartSubmitOK'),
    path('Ajaxaddress/',views.Ajaxaddress,name='Ajaxaddress'),
    path('Orderdetail/',views.Orderdetail,name='Orderdetail'),
    path('AjaxSaveCart/',views.AjaxSaveCart,name='AjaxSaveCart'),
]