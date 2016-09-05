# -*- coding:utf-8 -*-

from django.db import models
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=100)
    content = models.TextField()
    registered_date = models.DateTimeField(default=timezone.now)
    recruit_count = models.IntegerField()
    attend_count = models.IntegerField(default=1)
    recruit_status = models.IntegerField(default=0)  # 0:모집중, 1:모집완료
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100)
    address3 = models.CharField(max_length=100)
    comment_count = models.IntegerField(default=0)
    latlng = models.CharField(max_length=50, blank=True)
    meeting_date = models.DateTimeField(default=timezone.now)

    class Meta:
        # managed = False     # 자동으로 테이블을 생성하지 않게 된다
        ordering = ('-registered_date', )

    def __str__(self):
        return self.title

    def registered_comments(self):
        return self.comments.filter(post=self.pk)
    
    def as_json(self):
        return {
            'id': self.id,
            'author_id': self.author.id,
            'author_name': self.author.username,
            'title': self.title,
            'content': self.content,
            'recruit_count': self.recruit_count,
            'attend_list': self.participations.all(),
            'attend_count': self.attend_count,
            'comments': self.comments.all(),
            'comments_count': self.comments.all().count(),
            'registered_date': self.registered_date,
            'recruit_status': self.recruit_status,
        }

    @property
    def lat(self):
        if self.latlng:
            return self.latlng.split(',')[0]
        return None

    @property
    def lng(self):
        if self.latlng:
            return self.latlng.split(',')[1]
        return None

    def attend_users(self):
        participations = Participation.objects.filter(post=self)
        if participations:
            return list(i.user.username for i in participations)
        else:
            return []


class Comment(models.Model):
    post = models.ForeignKey('recruit.Post', related_name='comments')
    author = models.ForeignKey('auth.User')
    content = models.TextField()
    registered_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.content

    def as_json(self):
        return {
            'id': self.id,
            'content': self.content,
            'author_id': self.author.id,
            'author_name': self.author.username,
            'registered_date': self.registered_date,
        }


class Participation(models.Model):
    post = models.ForeignKey('recruit.Post', related_name='participations')
    user = models.ForeignKey('auth.User', related_name='users')

    class Meta:
        unique_together = ('post', 'user', )

    def __str__(self):
        return self.post.title

    def as_json(self):
        return {
            'id': self.id,
            'post_id': self.post.id,
            'user_id': self.user.id,
            'user_name': self.user.username,
        }
