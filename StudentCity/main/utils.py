menu = [{'title': "Главная страница", 'url_name': 'home'},
        {'title': "Студенты", 'url_name': 'students'},
        {'title': "Общежития", 'url_name': 'dorm'}]

class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        context['menu'] = menu
        return context