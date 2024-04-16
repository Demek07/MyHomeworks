# /cards/urls.py
from django.urls import path
from . import views

# Префикс /cards/
urlpatterns = [
    path('catalog/', views.catalog, name='catalog'),  # Общий каталог всех карточек
    path('categories/', views.get_categories, name='categories'),  # Список всех категорий
    path('categories/<int:category_id>/', views.get_cards_by_category, name='get_cards_by_category'),  # Карточки по категории
    path('tags/<int:tag_id>/', views.get_cards_by_tag, name='get_cards_by_tag'),  # Карточки по тегу
    path('<int:card_id>/detail/', views.get_detail_card_by_id, name='detail_card_by_id'),
    path('add/', views.add_card, name='add_card'),
    # path('search/', view.as_view(), name='search'),
]