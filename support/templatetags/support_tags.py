from django import template
from django.http import Http404

from support.models import *

register = template.Library()


@register.inclusion_tag('support/categories_list.html')
def show_categories(sort=None, cat_selected=0):
    if not sort:
        cats = Category.objects.all()
    else:
        cats = Category.objects.order_by(sort)

    return {"cats": cats, "cat_selected": cat_selected}


@register.inclusion_tag('support/post_list.html')
def show_posts(cat_selected=0):
    if cat_selected == 0:
        posts = Support.objects.filter(is_published=True)
    else:
        posts = Support.objects.filter(cat_id=cat_selected, is_published=True)

    return {"posts": posts, "cat_selected": cat_selected}


# @register.simple_tag(name='getcats')
# def get_categories(filter=None):
#     if not filter:
#         return Category.objects.all()
#     else:
#         return Category.objects.filter(pk=filter)


