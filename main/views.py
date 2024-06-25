from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .forms import UserRegistrationForm, UserLoginForm, LikeDislikeForm, CommentForm
from django.contrib.contenttypes.models import ContentType
from .models import LikeDislike, NewsItem, Comment
from django.http import JsonResponse
import requests
from django.views.decorators.http import require_POST


def index(request):
    return render(request, 'main/index.html')

def news(request):
    news_items = NewsItem.objects.all()
    comment_form = CommentForm()
    context = {
        'news_items': news_items,
        'comment_form': comment_form,
    }
    return render(request, 'main/news.html', context)

def add_comment(request, news_item_id):
    news_item = get_object_or_404(NewsItem, id=news_item_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.news_item = news_item
            comment.save()
            return redirect('news')
    return redirect('news')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserRegistrationForm()
    return render(request, 'main/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = UserLoginForm()
    return render(request, 'main/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('index')

@require_POST
def like_dislike(request):
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'status': 'fail', 'message': 'User not authenticated'})

    content_type = request.POST.get('content_type')
    object_id = request.POST.get('object_id')
    vote = request.POST.get('vote')

    content_type = ContentType.objects.get(model=content_type)
    content_object = content_type.get_object_for_this_type(id=object_id)

    like_dislike, created = LikeDislike.objects.get_or_create(
        content_type=content_type, object_id=object_id, user=user,
        defaults={'vote': vote}
    )

    if not created:
        if like_dislike.vote == int(vote):
            like_dislike.delete()
        else:
            like_dislike.vote = vote
            like_dislike.save()

    response = {
        'status': 'ok',
        'likes': content_object.total_likes(),
        'dislikes': content_object.total_dislikes(),
    }

    return JsonResponse(response)

def search_youtube(request):
    query = request.GET.get('query', 'music')
    api_key = 'AIzaSyDrxYK3bjDSB9KkDGvss4BoUaYzklpQAVw'
    url = f'https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&q={query}&key={api_key}'
    response = requests.get(url)
    results = response.json().get('items', [])

    context = {
        'results': results,
        'query': query
    }
    return render(request, 'main/youtube_search.html', context)
