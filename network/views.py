import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
import datetime
from .models import User, UserFollowing, Post, Comment, Like
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import ProfileForm, PostForm
@login_required
def search(request):
    query = request.GET.get('q')
    if query:
        users = User.objects.filter(Q(username__icontains=query) | Q(email__icontains=query))
    else:
        users = User.objects.none()

    return render(request, 'network/search_results.html', {
        'query': query,
        'users': users,
    })
def registerFunc(request):
    if request.method == "POST":
        # Retrieve user input from the registration form
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        
        # Check if passwords match
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        try:
            # Create a new user object and save it to the database
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        # Log the user in and redirect to the index page
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
    
def loginFunc(request):
    if request.method == "POST":
        # Retrieve user input from the login form
        username = request.POST["username"]
        password = request.POST["password"]
        
        # Authenticate user credentials
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # If authentication is successful, log the user in and redirect to the index page
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            # If authentication fails, render the login page with an error message
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")
    
@login_required
def index(request):
    error_message = None
    if request.method == "POST":
        post_body = request.POST.get("post", "").strip()
        if not post_body:
            error_message = "Post body cannot be empty"
            
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.comments = None
            post.save()
            return redirect('index')
    else:
        form = PostForm()
    
    # Retrieve all posts from the database, ordered by timestamp
    posts = Post.objects.all().order_by('-timestamp')
    
    # Paginate the posts
    p = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)
    
    return render(request, "network/index.html", {
        "form": form,
        "posts": page_obj,
        "pages": p,
        "error_message": error_message,
        
    })
@login_required
def logoutFunc(request):
    # Log the user out and redirect to the index page
    logout(request)
    return HttpResponseRedirect(reverse("index"))

@login_required
def comment(request, post_id):
    post = Post.objects.get(pk=post_id)

    # Handle deletion of user comments
    if "remove_comment" in request.POST:
        if request.POST["remove_comment"]:
            try:
                comment = Comment.objects.get(pk=request.POST['comment_id'])
                comment.delete()
            except Comment.DoesNotExist:
                return JsonResponse({"error": "Comment not found."}, status=404)

            comments = Comment.objects.filter(post=post)
            return render(request, "network/comment.html", {
                'post': post,
                'comments': comments
            })

    if request.method == "POST" and "post" in request.POST:
        # If a POST request is received, create a new comment
        comment_body = request.POST["post"]
        new_comment = Comment(comment=comment_body, user=request.user, post=post)
        new_comment.save()

    comments = Comment.objects.filter(post=post)
    return render(request, "network/comment.html", {
        'post': post,
        'comments': comments
    })
@login_required
def following(request):
    # Retrieve posts from followed users and paginate them
    user = User.objects.get(pk=request.user.id)
    followers = user.followers.all()
    posts = []

    if followers.exists():
        for follower in followers:
            posts.extend(Post.objects.filter(user=follower.user_id))

    posts = sorted(posts, key=lambda post: post.timestamp, reverse=True)

    p = Paginator(posts, 10)  
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)

    return render(request, "network/following.html", {
        "posts": page_obj,
        "pages": p
    })

@login_required
def like(request, post_id):
    if request.method == "POST":
        post = Post.objects.get(pk=post_id)

        try:
            like = Like.objects.get(user=request.user, post=post)
            print(like)
            if like and like.currently_liked == True:
                like.currently_liked = False
                post.total_likes -= 1
                post.user_likes.remove(request.user)
                post.save()           
                like.save()

                return HttpResponse(status=204)
            elif like and like.currently_liked == False:
                print('else', like)
                like.currently_liked = True
                post.total_likes += 1
                post.user_likes.add(request.user)
                post.save()
                like.save()

                return HttpResponse(status=204)
        

        except Like.DoesNotExist:
            new_like = Like(user=request.user, post=post, currently_liked=True)

            post.total_likes += 1
            post.user_likes.add(request.user)
            post.save()
            new_like.save()

            return HttpResponse(status=204)
    
    if request.method == "GET":
        print("GET METHOD")
        post = Post.objects.get(pk=post_id)
        print("NUMBER OF LIKES", post.total_likes)
        return JsonResponse(post.total_likes, safe=False)


@login_required
def post(request, post_id):

    if "remove_post" in request.POST:
        if request.POST["remove_post"]:
            post = Post.objects.get(user=request.user, pk=post_id)
            post.delete()
            return HttpResponseRedirect(reverse("index"))

    try:
        post = Post.objects.get(user=request.user, pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)
    
    if request.method == "PUT":
        data = json.loads(request.body)
        post.body = data['body']
        post.timestamp =  '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
        post.save()
        return HttpResponse(status=204)

@login_required
def user(request, user_id):
    requesting_user = get_object_or_404(User, pk=request.user.id)
    profile_user = get_object_or_404(User, pk=user_id)

    if request.method == "POST":
        if 'add_follow' in request.POST:
            follow_user(requesting_user, profile_user)
        elif 'remove_follow' in request.POST:
            unfollow_user(requesting_user, profile_user)

    followers = profile_user.followers.all()
    following = profile_user.following.all()
    followers_count = followers.count()
    following_count = following.count()
    is_following = UserFollowing.objects.filter(user_id=requesting_user, following_user_id=profile_user).exists()

    user_posts = Post.objects.filter(user=profile_user).order_by('-timestamp')
    paginator = Paginator(user_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/profile.html", {
        "user": profile_user,
        "following": following,
        "followers": followers,
        "followers_count": followers_count,
        "following_count": following_count,
        "posts": page_obj,
        "paginator": paginator,
        "requesting_user": requesting_user,
        "is_following": is_following
    })


def follow_user(follower, following_user):
    if not follower.following.filter(pk=following_user.id).exists():
        follower.following.add(following_user)
        following_user.followers.add(follower)
        follower.save()
        following_user.save()

def unfollow_user(follower, following_user):
    if follower.following.filter(pk=following_user.id).exists():
        follower.following.remove(following_user)
        following_user.followers.remove(follower)
        follower.save()
        following_user.save()
        
    
@login_required
def view_profile(request, user_id):
    profile_user = get_object_or_404(User, pk=user_id)

    if request.method == "POST":
        if 'add_follow' in request.POST:
            UserFollowing.objects.get_or_create(user_id=request.user.id, following_user_id=profile_user.id)
        elif 'remove_follow' in request.POST:
            UserFollowing.objects.filter(user_id=request.user.id, following_user_id=profile_user.id).delete()

    followers_count = profile_user.followers.count()
    following_count = profile_user.following.count()
    is_following = UserFollowing.objects.filter(user_id=request.user.id, following_user_id=profile_user.id).exists()

    user_posts = Post.objects.filter(user=profile_user).order_by('-timestamp')
    paginator = Paginator(user_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/other_user_profile.html", {
        "profile_user": profile_user,
        "followers_count": followers_count,
        "following_count": following_count,
        "posts": page_obj,
        "is_following": is_following
    })
def follow_user(requesting_user, user_to_follow):
    if not UserFollowing.objects.filter(user_id=requesting_user, following_user_id=user_to_follow).exists():
        UserFollowing.objects.create(user_id=requesting_user, following_user_id=user_to_follow)

def unfollow_user(requesting_user, user_to_unfollow):
    follow_instance = UserFollowing.objects.filter(user_id=requesting_user, following_user_id=user_to_unfollow)
    if follow_instance.exists():
        follow_instance.delete()
        
@login_required
def edit_profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user', user_id=user.id)  # Redirect to the user's profile page
    else:
        form = ProfileForm(instance=user)

    return render(request, 'network/edit_profile.html', {'profile_form': form})