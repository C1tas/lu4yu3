from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.template.defaultfilters import slugify

# Create your models here.


class Article(models.Model):
    def return_list(tmp_list):
        return tmp_list
    url = models.URLField()
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    title_zh = models.CharField(max_length=100, unique=True)
    author = models.CharField(max_length=100)
    content_md = models.TextField()
    content_html = models.TextField()
    content_toc = models.TextField()
    tags = ArrayField(models.CharField(max_length=40),
                      default=return_list([':D']))
    categories = ArrayField(models.CharField(max_length=40),
                            default=return_list([':D']))
    views = models.IntegerField(default=0)
    created = models.DateTimeField(db_index=True, auto_now_add=True)
    updated = models.DateTimeField(db_index=True, auto_now_add=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        self.title_zh = self.title
        if TCList.objects.count() == 0:
            TCList.objects.create(tag_list=[], cate_list=[])
        else:
            pass
        tc_list = TCList.objects.first()
        tc_list.tag_list.extend(self.tags)
        tc_list.tag_list = list(TCList.dedupe(tc_list.tag_list))
        tc_list.cate_list.extend(self.categories)
        tc_list.cate_list = list(TCList.dedupe(tc_list.cate_list))
        tc_list.save()
        super(Article, self).save(*args, **kwargs)  # call Django's save()


class TCList(models.Model):
    tag_list = ArrayField(models.CharField(max_length=40))
    cate_list = ArrayField(models.CharField(max_length=40))

    def dedupe(items):
        seen = set()
        for item in items:
            if item not in seen:
                yield item
            seen.add(item)
