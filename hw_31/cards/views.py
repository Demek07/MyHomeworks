from django.db.models import F
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template.context_processors import request
from .models import Card


info = {
    "users_count": 100500,
    "cards_count": 200600,
    # "menu": ['Главная', 'О проекте', 'Каталог']
    "menu": [
        {"title": "Главная",
         "url": "/",
         "url_name": "index"},
        {"title": "Каталог",
         "url": "/cards/catalog/",
         "url_name": "catalog"},
        {"title": "О проекте",
         "url": "/about/",
         "url_name": "about"},
    ]
}


def index(request):
    """Функция для отображения главной страницы
    будет возвращать рендер шаблона root/templates/main.html"""
    return render(request, "main.html", info)


def about(request):
    """Функция для отображения страницы "О проекте"
    будет возвращать рендер шаблона /root/templates/about.html"""
    return render(request, 'about.html', info)


def catalog(request):
    # По умолчанию сортируем по дате загрузки
    sort = request.GET.get('sort', 'upload_date')
    # По умолчанию сортируем по убыванию
    order = request.GET.get('order', 'desc')

    valid_sort_fields = {'upload_date', 'views', 'adds'}
    if sort not in valid_sort_fields:
        sort = 'upload_date'
    if order == 'asc':
        order_by = sort
    else:
        order_by = f'-{sort}'

    cards = Card.objects.all().order_by(order_by)

    context = {
        'cards': cards,
        'cards_count': cards.count(),
        'menu': info['menu'],
    }

    return render(request, 'cards/catalog.html', context)



def get_categories(request):
    """
    Возвращает все категории для представления в каталоге
    """
    # Проверка работы базового шаблона
    return render(request, 'base.html', info)


def get_cards_by_category(request, slug):
    """
    Возвращает карточки по категории для представления в каталоге
    """
    return HttpResponse(f'Cards by category {slug}')


def get_cards_by_tag(request, slug):
    """
    Возвращает карточки по тегу для представления в каталоге
    """
    return HttpResponse(f'Cards by tag {slug}')


def get_detail_card_by_id(request, card_id):
    """
    Возвращает детальную информацию по карточке для представления
    Использует функцию get_object_or_404 для обработки ошибки 404
    """

    # Добываем карточку из БД через get_object_or_404
    # если карточки с таким id нет, то вернется 404
    card = get_object_or_404(Card, pk=card_id)

    # Обновляем счетчик просмотров через F object
    card.views = F('views') + 1
    card.save()

    card.refresh_from_db()  # Обновляем данные из БД

    # Подготавливаем контекст и отображаем шаблон
    context = {
        'card': card,
        'menu': info['menu'],
    }

    return render(request, 'cards/card_detail.html', context)