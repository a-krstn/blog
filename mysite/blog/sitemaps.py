from django.contrib.sitemaps import Sitemap
from .models import Post


class PostSitemap(Sitemap):
    changefreq = 'weekly'   # частота изменения страниц постов
    priority = 0.9          # релевантность страниц постов

    def items(self):
        return Post.published.all()

    def lastmod(self, obj):
        """возвращает время последнего изменения объекта"""
        return obj.updated
