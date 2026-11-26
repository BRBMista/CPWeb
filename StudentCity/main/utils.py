import re
from rest_framework.pagination import PageNumberPagination

menu = [{'title': "Главная страница", 'url_name': 'home'},
        {'title': "Студенты", 'url_name': 'students'},
        {'title': "Общежития", 'url_name': 'dorm'}]


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        context['menu'] = menu
        return context


class StudentAPIPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 20


TRANSLIT = {
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e',
    'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
    'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
    'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch',
    'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
}


def make_slug(text):
    text = ''.join(TRANSLIT.get(ch, ch) for ch in text.lower())
    text = re.sub(r'[^a-z0-9]+', '-', text).strip('-')
    return text or 'student'


def unique_slug(model, text):
    base = make_slug(text)
    slug = base
    number = 2
    while model.objects.filter(slug=slug).exists():
        slug = f'{base}-{number}'
        number += 1
    return slug
