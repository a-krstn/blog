from django import template
from ..models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

register = template.Library()   # для регистрации шаблонных тегов и фильтров


@register.simple_tag
def total_posts():      # имя функции будет именем тега, но в декораторе можно прописать (name='my_tag')
    return Post.published.count()


@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=3):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


@register.simple_tag
def get_most_commented_posts(count=3):
    res = Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]
    return res


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
