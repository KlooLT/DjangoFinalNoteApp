from django .urls import path
from django.contrib.auth.views import LogoutView
from .views import NoteList, NoteDetail, NoteCreate, NoteUpdate, NoteDeleteView, LoginViewNew, SignUpPage, CategoryCreate, CategoryViewList, CategoryUpdate
from . import views

urlpatterns = [
    path('login/', LoginViewNew.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', SignUpPage.as_view(), name='register'),
    path('', NoteList.as_view(), name='notes'),
    path('note/<int:pk>/', NoteDetail.as_view(), name='note'),
    path('note-create/', NoteCreate.as_view(), name='note-create'),
    path('note-update/<int:pk>/', NoteUpdate.as_view(), name='note-update'),
    path('note-delete/<int:pk>/', NoteDeleteView.as_view(), name='note-delete'),
    path('category-create/', CategoryCreate.as_view(), name='category-create'),
    path('category/', CategoryViewList, name='category'),
    path('categories/<str:pk>/delete', views.CategoryDeleteView.as_view(), name='category-delete'),
    path('category-update/<int:pk>/', CategoryUpdate.as_view(), name='category-update'),
]
