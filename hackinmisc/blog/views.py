from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.template.defaultfilters import slugify
from django.db import models
from django.conf import settings

from bs4 import BeautifulSoup

from .models import Article, TCList
from .forms import  ArticlePublishApiForm

import markdown
import datetime
# Create your views here.


def index(request):
    try:
        article_list = Article.objects.order_by('-created')[:3]
    except:
        article_list = []
    try:
        tag_list = TCList.objects.first().tag_list
        cate_list = TCList.objects.first().cate_list
    except:
        tag_list = []
        cate_list = []

    return render(request, 'blog/index.pug.bak', {'posts': article_list,
                                                  'tags': tag_list,
                                                  'categories': cate_list,})

def home(request):
    try:
        article_list = Article.objects.order_by('-created')[:3]
    except:
        article_list = []
    try:
        tag_list = TCList.objects.first().tag_list
        cate_list = TCList.objects.first().cate_list
    except:
        tag_list = []
        cate_list = []

    return render(request, 'blog/home.pug', {'posts': article_list,
                                             'tags': tag_list,
                                             'categories': cate_list,})

# func for next pages
def pages(requests):
    pass

def post(request, slug):
    cur_article = Article.objects.get(slug = slug)
    if cur_article:
        return render(request, 'blog/post.pug', {'post': cur_article})
    pass


def publish_article(request):
    if request.method == 'POST':
        tmp_form = ArticlePublishApiForm(request.POST)
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
