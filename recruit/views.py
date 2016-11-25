# -*- coding: utf-8 -*-

from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token

from basket_together.json_data_format import *
from recruit.forms import PostForm, CommentForm
from recruit.models import Post, Comment, Participation

MESSAGE_POST_ADD = '글이 등록 되었습니다.'
MESSAGE_POST_EDIT = '글이 수정 되었습니다.'
MESSAGE_POST_DELETE = '글이 삭제 되었습니다.'
MESSAGE_COMMENT_ADD = '댓글이 등록 되었습니다.'
MESSAGE_COMMENT_EDIT = '댓글이 수정 되었습니다.'
MESSAGE_COMMENT_DELETE = '댓글이 삭제 되었습니다.'


# token 값으로 유저 출력
def get_user_in_token(request):
    token_ = Token.objects.get(pk=request.META.get('HTTP_TOKEN'))
    return token_.user


@csrf_exempt
def post_list_all(request):
    posts = Post.objects.all()
    if posts.exists():
        return posts
    else:
        return JsonResponse({})


@csrf_exempt
def post_list(request, page=1):
    posts = Post.objects.all()
    paginator = Paginator(posts, 10)
    page_range = paginator.page_range

    try:
        contacts = paginator.page(page)
    except EmptyPage:
        return output_format_json_response(message='해당 페이지가 없습니다.')

    args = dict()
    # args.update(request)
    args['post_list'] = contacts.object_list
    args['total_page'] = paginator.num_pages
    args['total_count'] = posts.count()
    return args


@csrf_exempt
def post_add(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = get_user_in_token(request)
            post.save()
            add_participation(request, post.id)
            return output_format_json_response(201, message=MESSAGE_POST_ADD)
        else:
            return output_format_json_response(400, message=form.errors)
    return output_format_json_response(message='POST로 요청해 주십시요.')


@csrf_exempt
def post_detail(request, pk):

    if request.method == 'GET':
        return get_object_or_404(Post, pk=pk)
    elif request.method == 'PUT':
        post = get_object_or_404(Post, pk=pk)
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post.save()
            return output_format_json_response(201, message=MESSAGE_POST_EDIT)
    elif request.method == 'DELETE':
        post = get_object_or_404(Post, pk=pk)
        post.delete()
        return output_format_json_response(204, message=MESSAGE_POST_DELETE)


@csrf_exempt
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = get_user_in_token(request)
        comment.post = post
        comment.save()
        return output_format_json_response(201, message=MESSAGE_COMMENT_ADD)
    else:
        return JsonResponse(form.errors)


@csrf_exempt
def comments_to_post(request, pk):
    post = Post.objects.get(pk=pk)
    comments = Comment.objects.filter(post=post)
    return comments


@csrf_exempt
def post_search(request):
    word = request.POST.get('word')
    posts = Post.objects.filter(title__contains=word) or Post.objects.filter(content__contains=word)
    return posts


def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return output_format_json_response(204, message=MESSAGE_COMMENT_DELETE)


def add_participation(request, pk):
    user_ = get_user_in_token(request)
    post = get_object_or_404(Post, pk=pk)
    next_url = request.GET.get('next', '')
    Participation.objects.create(post=post, user=user_)
    post.attend_count += 1
    post.save()
    return output_format_json_response(201, message='참여가 완료 되었습니다.')


def remove_participation(request, pk):
    user_ = get_user_in_token(request)
    post = get_object_or_404(Post, pk=pk)
    bookmark = get_object_or_404(Participation, post=post, user=user_)
    bookmark.delete()
    post.attend_count -= 1
    post.save()
    return output_format_json_response(201, message='참여가 취소 되었습니다.')
