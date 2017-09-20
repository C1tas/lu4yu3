from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.template.defaultfilters import slugify
from django.conf import settings
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView

from bs4 import BeautifulSoup

from .models import Article, TCList
from .forms import ArticlePublishApiForm

import markdown
import datetime
import math
# Create your views here.


def index(request):
    return redirect('/!home')


class HomeView(ListView):
    model = Article
    template_name = 'blog/home.pug'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        # cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(HomeView, self).get_queryset().filter(type='post')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')
        pagination_data = self.pagination_data(paginator, page, is_paginated)
        context.update(pagination_data)
        return context

    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            return {}

        left = []
        right = []
        left_has_more = False
        right_has_more = False
        first = False
        last = False

        page_has_next = page.has_next()
        page_has_previous = page.has_previous()
        page_number = page.number
        total_pages = paginator.num_pages
        page_range = paginator.page_range

        if page_number == 1:
            right = page_range[page_number:page_number + 2]
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True

        elif page_number == total_pages:
            # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 left = [2, 3]
            # 这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]

            if left[0] > 2:
                left_has_more = True

            if left[0] >= 1:
                first = True
        else:
            left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
            right = page_range[page_number:page_number + 2]

            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True

            if left[0] > 2:
                left_has_more = True
            if left[0] >= 1:
                first = True

        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
            'has_previous': page_has_previous,
            'has_next': page_has_next,
        }
        # print(data)
        return data


class DailyView(HomeView):
    def get_queryset(self):
        # cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(HomeView, self).get_queryset().filter(type='daily')


class PostView(DetailView):
    model = Article
    template_name = 'blog/post.pug'
    context_object_name = 'post'


def publish_article(request):
    if request.method == 'POST':
        tmp_form = ArticlePublishApiForm(request.POST)
        if tmp_form.is_valid():
            tmp_article = tmp_form.save(commit=False)
            md = markdown.Markdown(extensions=['markdown.extensions.toc(baselevel=3)'])
            tmp_article.content_html = md.convert(tmp_article.content_md)
            soup = BeautifulSoup(md.toc, 'html.parser')
            soup.ul['class'] = 'section table-of-contents pinned'
            tmp_article.author = 'C1tas'
            tmp_article.content_toc = str(soup)
            # tmp_article.categories = tmp_article.categories.split(',')
            # tmp_article.tags = tmp_article.tagg.split(',')
            tmp_article.save()
            tmp_form.save_m2m()

    else:
        tmp_form = ArticlePublishApiForm()
    return render(request, 'blog/publish.pug', {'form': tmp_form})


@csrf_exempt
def api_publish_article(request):
    print(request.method)
    if request.method == 'POST':
        tmp_form = ArticlePublishApiForm(request.POST)
        if tmp_form.is_valid():
            tmp_article = tmp_form.save(commit=False)
            tmp_article.content_html = markdown.markdown(tmp_article.content_md)
            tmp_article.author = 'C1tas'
            tmp_article.save()
            tmp_form.save_m2m()
            return HttpResponse('success')
    else:
        return HttpResponse('api')


@csrf_exempt
def api_update_article(request):
    print(request.method)
    if request.method == 'POST':
        if 'secret_key' in request.POST:
            if request.POST['secret_key'] == settings.SECRET_KEY:
                # del request.POST['secret_key']
                tmp_form = ArticlePublishApiForm(request.POST)
            else:
                tmp_form = ArticlePublishApiForm()
        else:
            return HttpResponse("permission denied")

        if tmp_form.is_valid():
            tmp_article = tmp_form.save(commit=False)
            md = markdown.Markdown(extensions=['markdown.extensions.toc(baselevel=2)','markdown.extensions.codehilite','markdown.extensions.extra','markdown.extensions.meta'])
            tmp_article.content_html = md.convert(tmp_article.content_md)
            soup = BeautifulSoup(tmp_article.content_html, 'html.parser')
            h_tag = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5'])
            for i in h_tag:
                i['class'] = ['section','scrollspy']
            tmp_article.content_html = soup.prettify()
            # return HttpResponse(str(md.Meta))
            if 'title' in md.Meta:
                tmp_article.title = md.Meta['title'][0]
            else:
                return HttpResponse("Your post needs title")
            if 'tag' in md.Meta:
                tmp_article.tags = md.Meta['tag']
            else:
                return HttpResponse("Your post needs one tag at least")
            if 'category' in md.Meta:
                tmp_article.categories = md.Meta['category']
            else:
                return HttpResponse("Your post needs one category at leasts")
            if 'author' in md.Meta:
                tmp_article.author = md.Meta['author'][0]
            if 'summary' in md.Meta:
                tmp_article.summary = md.Meta['summary'][0]
            if 'type' in md.Meta:
                tmp_article.type = md.Meta['type'][0]
            if not md.toc:
                return HttpResponse("Your post looks strange~")

            try:
                cur_article = Article.objects.get(slug=slugify(tmp_article.title))
                cur_article.content_html = tmp_article.content_html
                cur_article.title = tmp_article.title
                cur_article.tags = tmp_article.tags
                cur_article.summary = tmp_article.summary
                cur_article.categories = tmp_article.categories
                cur_article.content_md = tmp_article.content_md
                cur_article.author = tmp_article.author
                cur_article.type = tmp_article.type
                soup = BeautifulSoup(md.toc, 'html.parser')
                if soup.ul:
                    soup.ul['class'] = 'section table-of-contents pinned'
                cur_article.content_toc = str(soup)
                cur_article.updated = datetime.datetime.now()
                cur_article.save()
                return HttpResponse('exist')
            except Article.DoesNotExist:
                soup = BeautifulSoup(md.toc, 'html.parser')
                if soup.ul:
                    soup.ul['class'] = 'section table-of-contents pinned'
                tmp_article.content_toc = str(soup)
                tmp_article.updated = datetime.datetime.now()
                tmp_article.save()
                tmp_form.save_m2m()

            return HttpResponse('valid')

            return HttpResponse('success')
    else:
        return HttpResponse('api')
