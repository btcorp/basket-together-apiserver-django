# -*- coding: utf-8 -*-

import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from recruit.models import Post, Comment, Participation
from recruit.forms import PostForm, CommentForm
from rest_framework.authtoken.models import Token

MESSAGE_POST_ADD = '글이 등록 되었습니다.'
MESSAGE_POST_EDIT = '글이 수정 되었습니다.'
MESSAGE_POST_DELETE = '글이 삭제 되었습니다.'
MESSAGE_COMMENT_ADD = '댓글이 등록 되었습니다.'
MESSAGE_COMMENT_EDIT = '댓글이 수정 되었습니다.'
MESSAGE_COMMENT_DELETE = '댓글이 삭제 되었습니다.'


# byte to string 헬퍼 메서드
def decoding_byte_to_string(byte_data):
    bytes_to_string = byte_data.decode('utf-8')
    return json.loads(bytes_to_string)


# token 값으로 유저 출력
def get_user_in_token(token):
    token_ = Token.objects.get(pk=token)
    return token_.user


def post_list_all(request):
    posts = Post.objects.all()
    if posts.exists():
        return posts
    else:
        return JsonResponse({})


def post_list(request, page=1):
    try:
        posts = Post.objects.all()
        paginator = Paginator(posts, 3)
        page_range = paginator.page_range
        contacts = paginator.page(page)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)
    except ObjectDoesNotExist:
        contacts = None
        return JsonResponse({'message': 'Empty object'})

    args = dict()
    args.update(request)
    args['object_list'] = contacts.object_list
    args['num_pages'] = paginator.num_pages
    args['post_count'] = posts.count()
    # args['page'] = page
    # return JsonResponse([i.as_json() for i in contacts.object_list], safe=False)
    # return contacts.object_list
    return args


@csrf_exempt
def post_add(request):
    if request.method == 'POST':
        data = decoding_byte_to_string(request.body)
        form = PostForm(data)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = get_user_in_token(request.META.get('HTTP_TOKEN'))
            post.save()
            return JsonResponse({'message': MESSAGE_POST_ADD}, status=201)
        else:
            return JsonResponse(form.errors, status=400)
    return JsonResponse({'message': 'POST로 요청해 주십시요.'})


@csrf_exempt
def post_detail(request, pk):

    if request.method == 'GET':
        return get_object_or_404(Post, pk=pk)
    elif request.method == 'PUT':
        data = decoding_byte_to_string(request.body)
        post = get_object_or_404(Post, pk=pk)
        form = PostForm(data, instance=post)
        if form.is_valid():
            post.save()
            return JsonResponse({'message': MESSAGE_POST_EDIT}, status=201)
    elif request.method == 'DELETE':
        post = get_object_or_404(Post, pk=pk)
        post.delete()
        return JsonResponse({'message': MESSAGE_POST_DELETE}, status=204)


@csrf_exempt
def add_comment_to_post(request, pk):
    data = decoding_byte_to_string(request.body)
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm(data)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = get_user_in_token(request.META.get('HTTP_TOKEN'))
        comment.post = post
        comment.save()
        return JsonResponse({'message': MESSAGE_COMMENT_ADD})
    else:
        return JsonResponse(form.errors)


def comments_to_post(request, pk):
    post = Post.objects.get(pk=pk)
    comments = Comment.objects.filter(post=post)
    return comments


@csrf_exempt
def post_search(request):
    data = decoding_byte_to_string(request.body)
    word = data['word']
    posts = Post.objects.filter(title__contains=word) or Post.objects.filter(content__contains=word)
    return posts


def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return JsonResponse({'message': MESSAGE_COMMENT_DELETE}, status=204)


def add_participation(request, pk):
    user_ = get_user_in_token(request.META.get('HTTP_TOKEN'))
    post = get_object_or_404(Post, pk=pk)
    next_url = request.GET.get('next', '')
    Participation.objects.create(post=post, user=user_)
    post.attend_count += 1
    post.save()
    return JsonResponse({'message': '참여가 완료 되었습니다.', 'next_url': next_url}, status=201)


def remove_participation(request, pk):
    user_ = get_user_in_token(request.META.get('HTTP_TOKEN'))
    post = get_object_or_404(Post, pk=pk)
    bookmark = get_object_or_404(Participation, post=post, user=user_)
    bookmark.delete()
    post.attend_count -= 1
    post.save()
    return JsonResponse({'message': '참여가 취소 되었습니다.'}, status=204)