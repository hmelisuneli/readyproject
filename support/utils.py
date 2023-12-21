from django.db.models import Count
from django.core.cache import cache
from .models import *

menu = [{'title': "About us", 'url_name': 'about'},
        {'title': "Contacts", 'url_name': 'contact'},
        ]


class DataMixin:
    paginate_by = 3

    def get_user_context(self, **kwargs):

        context = kwargs
        cats = Category.objects.annotate(Count('support'))

        # cats=cache.get('cats')
        # if not cats:
        #     cats=Category.objects.annotate(Count('support'))
        #     cache.set('cats',cats,60)

        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)

        context['menu'] = user_menu

        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context
