import ast
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from recruit.models import Post, Comment
from recruit.forms import PostForm, CommentForm

"""
class JSONListView(ListView):
    queryset = Post.objects.all()

    def get(self, request, *args, **kwargs):
        return JsonResponse(list(self.get_queryset().values()), safe=False)


def jsonFormResponse(data):
    return JsonResponse(
        data, 
        safe=False, 
        json_dumps_params={
            'ensure_ascii':False,
            'separators':(',',':'), 
            'sort_keys':True, 
            'indent':4
        }
    )


def post_list(request):
    # posts = Post.objects.all()
    posts = Post.objects.all().values(
            'id', 'title', 'content', 'recruit_count',
            'attend_count', 'comment_count', 'registered_date',
    )
    return jsonFormResponse(list(posts))
"""


def post_list(request):
    return Post.objects.all()


@csrf_exempt
def post_add(request):
    if request.method == 'POST':
        # bytes_to_dict = dict((request.body).decode('utf-8'))
        byte_to_str = (request.body).decode('utf-8')
        data = ast.literal_eval(byte_to_str)
        form = PostForm(data)
        if form.is_valid():
            post = form.save(commit=False)
            user = get_user_model().objects.first()
            post.author = user
            post.save()
            return post


def post_detail(request, pk):
    return get_object_or_404(Post, pk=pk)


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('recruit.views.post_detail', pk=pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'recruit/post_edit.html', {'form': form})


def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('recruit.views.post_list')


@csrf_exempt
def add_comment_to_post(request, pk):
    byte_to_str = (request.body).decode('utf-8')
    data = ast.literal_eval(byte_to_str)
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm(content=data['content'])

    if form.is_valid():
        try:
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return JsonResponse({'message': 'Comments were registed.'})
        except ObjectDoesNotExist:
            return JsonResponse({'message': 'Comments were not registed.'})
    else:
        return JsonResponse({'message': 'Form data is invalid.'})


def comments_to_post(request, pk):
    post = Post.objects.get(pk=pk)
    comments = Comment.objects.filter(post=post)
    return comments


def post_search(request):
    word = request.POST['word']
    posts = Post.objects.filter(title__contains=word) or Post.objects.filter(content__contains=word)
    return render(request, 'recruit/post_list.html', {'posts': posts})


def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('recruit.views.post_detail', pk=post_pk)
