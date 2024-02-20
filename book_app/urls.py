from django.urls import path
from book_app import views
from book_app import rest_views

urlpatterns = [
    path('home/', views.index, name='home'),
    path('booklist/',views.book_list, name='booklist'),
    path('book/<int:pk>',views.book_detail, name='bookdetail'),
    path('contact/',views.contact, name='contact'),
    path('about/',views.about, name='about'),
    path('add_to_cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('cart/',views.cart, name='cart'),
    path('checkout/',views.checkout, name='checkout'),
    path('process_payment/<str:order_id>/', views.process_payment, name='process_payment'),
    
    #Rest_api urls
    
    path('api/books/', rest_views.BookListView.as_view(), name='book_list'),
    path('api/books/<int:pk>/', rest_views.BookDetailView.as_view(), name='book_detail'),
    path('api/orders/<int:customer>/', rest_views.OrderListView.as_view(), name='order_list'),
]
