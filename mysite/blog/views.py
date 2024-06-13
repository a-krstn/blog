from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.db.models import Count
from taggit.models import Tag
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

from .models import *
from .forms import EmailPostForm, CommentForm, SearchForm
# from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView


def post_list(request, tag_slug=None):
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)            # если страницы с таким номером нет, то будет 1 страница
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)     # выдаст последнюю страницу
    context = {'posts': posts, 'tag': tag}
    return render(request, 'blog/post/list.html', context)


# class PostListView(ListView):
#     queryset = Post.published.all()     # форм-ем конкретно-прикладной набор запросов вместо model = Post
#     context_object_name = 'posts'       # в posts запишется результат запроса, можно юзать в шаблонах
#     paginate_by = 3
#     template_name = 'blog/post/list.html'   # задается название шаблона


def post_detail(request, day, month, year, post):
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__day=day,
                             publish__month=month,
                             publish__year=year)     # функция сокращенного доступа
    comments = post.comments.filter(active=True)     # список активных комментариев к посту
    form = CommentForm()
    post_tags_ids = post.tags.values_list('id', flat=True)  # список идентификаторов тегов текущего поста
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)   # все посты, где такой же тег
    # Count генерирует поле same_tags, содержащее число тегов, общих со всеми запрошенными тегами
    # результат упорядочивается по числу общих тегов и по publish, чтобы отображать последние посты
    # получаем только первые 4 поста
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
    context = {
        'post': post,
        'comments': comments,
        'form': form,
        'similar_posts': similar_posts,
    }
    return render(request, 'blog/post/detail.html', context)


def post_share(request, post_id):
    post = get_object_or_404(Post,
                             id=post_id,
                             status=Post.Status.PUBLISHED)

    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} рекомендует вам прочитать {post.title}"
            message = f"Прочтите статью {post.title} по ссылке {post_url} {cd['name']} комментирует: {cd['comments']}"
            send_mail(subject, message, 'your_account@gmail.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    context = {'post': post, 'form': form, 'sent': sent}
    return render(request, 'blog/post/share.html', context)


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post,
                             id=post_id,
                             status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)   # созд-ие об-а класса Comment, не сохр-яя его в БД
        comment.post = post                 # назначение поста комментарию
        comment.save()                      # сохр-ие коммент-я в БД
    context = {'post': post, 'form': form, 'comment': comment}
    return render(request, 'blog/post/comment.html', context)


def post_search(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
            search_query = SearchQuery(query, config='russian')
            results = Post.published.annotate(
                search=search_vector,
                rank=SearchRank(search_vector, search_query)
            ).filter(rank__gte=0.3).order_by('-rank')

    return render(request,
                  'blog/post/search.html',
                  {'form': form,
                   'query': query,
                   'results': results})
