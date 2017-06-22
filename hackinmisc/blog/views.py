from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.template.defaultfilters import slugify
from django.db import models

from bs4 import BeautifulSoup

from .models import Article, TCList
from .forms import  ArticlePublishForm


import markdown
import datetime
# Create your views here.


def index(request):
    try:
        article_list = Article.objects.order_by('-created')[:5]
    except:
        article_list = []
    try:
        tag_list = TCList.objects.first().tag_list
        cate_list = TCList.objects.first().cate_list
    except:
        tag_list = []
        cate_list = []

    return render(request, 'blog/index.pug', {'posts': article_list,
                                              'tags': tag_list,
                                              'categories': cate_list,
                                              })

def post(request, slug):
    cur_article = Article.objects.get(slug = slug)
    if cur_article:
        return render(request, 'blog/post.pug', {'post': cur_article})
    pass


def publish_article(request):
    if request.method == 'POST':
        tmp_form = ArticlePublishForm(request.POST)
        if tmp_form.is_valid():
            tmp_article = tmp_form.save(commit=False)
            md = markdown.Markdown(extensions=['markdown.extensions.toc(baselevel=3)'])
            tmp_article.content_html = md.convert(tmp_article.content_md)
            soup = BeautifulSoup(md.toc ,'html.parser')
            soup.ul['class'] = 'section table-of-contents pinned'
            tmp_article.author = 'C1tas'
            tmp_article.content_toc = str(soup)
            # tmp_article.categories = tmp_article.categories.split(',')
            # tmp_article.tags = tmp_article.tagg.split(',')
            tmp_article.save()
            tmp_form.save_m2m()

    else:
        tmp_form = ArticlePublishForm()
    return render(request, 'blog/publish.pug', {'form': tmp_form})


@csrf_exempt
def api_publish_article(request):
    print(request.method)
    if request.method == 'POST':
        tmp_form = ArticlePublishForm(request.POST)
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
        tmp_form = ArticlePublishForm(request.POST)
        if tmp_form.is_valid():
            tmp_article = tmp_form.save(commit=False)
            md = markdown.Markdown(extensions=['markdown.extensions.toc(baselevel=2)','markdown.extensions.codehilite','markdown.extensions.extra'])
            try:
                cur_article = Article.objects.get(slug=slugify(tmp_article.title))
                cur_article.content_md = tmp_article.content_md
                cur_article.content_html = md.convert(tmp_article.content_md)
                soup = BeautifulSoup(md.toc, 'html.parser')
                if soup.ul:
                    soup.ul['class'] = 'section table-of-contents pinned'
                cur_article.content_toc = str(soup)
                cur_article.updated = datetime.datetime.now()
                cur_article.save()
                return HttpResponse('exist')
            except Article.DoesNotExist:
                tmp_article.content_html = md.convert(tmp_article.content_md)
                soup = BeautifulSoup(md.toc, 'html.parser')
                if soup.ul:
                    soup.ul['class'] = 'section table-of-contents pinned'
                tmp_article.content_toc = str(soup)
                tmp_article.author = 'C1tas'
                tmp_article.save()
                tmp_form.save_m2m()

            return HttpResponse('valid')

            tmp_article = tmp_form.save(commit=False)
            tmp_article.content_html = markdown.markdown(tmp_article.content_md)
            tmp_article.author = 'C1tas'
            tmp_article.save()
            tmp_form.save_m2m()
            return HttpResponse('success')
    else:
        return HttpResponse('api')
