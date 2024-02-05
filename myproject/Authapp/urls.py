from django.urls import path
from . import views

urlpatterns = [
    path('authsetApi/', views.authsetApi.as_view(), name='authsetApi'),
    path('BookApi/', views.BookApi.as_view(), name='BookApi'),
    path('', views.login_ren, name="login_ren"),
    path('login_admin/', views.login_admin, name="login_admin"),
    path('author/', views.auther_view, name="author_view"),
    path('logout_view/', views.logout_view, name="logout_view"),
    path('save_author_data/', views.save_author_data, name="save_author_data"),
    path('search/', views.search_results, name='search_results'),
    path('edit_author/', views.edit_author, name='edit_author'),
    path('book_view/', views.book_view, name='book_view'),
    path('save_book_data/', views.save_book_data, name='save_book_data'),
    path('book_search_results/', views.book_search_results, name='book_search_results'),
    path('edit_book/', views.edit_book, name='edit_book'),
    path('author_detailed_view/<int:id>/', views.author_detailed_view, name='author_detailed_view'),
    path('edit_author_book/', views.edit_author_book, name='edit_author_book'),
    path('edit_author_old_book/', views.edit_author_old_book, name='edit_author_old_book'),
    path('author_bk_search/', views.author_bk_search, name='author_bk_search'),
    path('AuthorDetailsAPI/', views.AuthorDetailsAPI.as_view(), name='AuthorDetailsAPI'),
    path('AuthorUpdationApi/<int:pk>/',views.AuthorUpdationApi.as_view(), name='AuthorUpdationApi'),
    path('BookDetailsAPI/', views.BookDetailsAPI.as_view(), name='BookDetailsAPI'),
    path('BookUpdationApi/<int:id>/', views.BookUpdationApi.as_view(), name='BookUpdationApi'),
    path('toggle_status_change/', views.toggle_status_change, name='toggle_status_change'),
    path('toggle_status_change_book/', views.toggle_status_change_book, name='toggle_status_change_book'),


]
