from django.urls import path, include
from . import views

urlpatterns = [
    path('books/', views.book_list),
    path('books/<int:pk>/', views.book_detail),  # wpisujemy id/pk ksiazki, do ktorej chcemy sie dostac
    path("books_cbv/", views.BookListView.as_view(), name="book-list"),
    path("books_cbv/<int:pk>/", views.BookDetailView.as_view(), name="book-detail"),  # cbv od class base view
]