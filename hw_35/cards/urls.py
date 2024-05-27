# /cards/urls.py
from django.urls import path
from . import views

# Префикс /cards/
urlpatterns = [
    path('catalog/', views.CatalogView.as_view(), name='catalog'),  # Общий каталог всех карточек
    path('categories/', views.get_categories, name='categories'),  # Список всех категорий
    path('categories/<int:category_id>/', views.get_cards_by_category, name='get_cards_by_category'),  # Карточки по категории
    path('tags/<int:tag_id>/', views.get_cards_by_tag, name='get_cards_by_tag'),  # Карточки по тегу
    path('<int:pk>/detail/', views.CardDetailView.as_view(), name='detail_card_by_id'),
    path('add/', views.AddCardCreateView.as_view(), name='add_card'),
]