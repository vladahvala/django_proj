from django.shortcuts import render, redirect
from .models import Post, Profile, Comment, Category
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import ProfileForm, AddCommentForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required

# Create your views here.
#дані збираються з бази даних, відправляються на html-сторінку, потім рендеряться(готуються) і відправляються назад користувачу

def blog_main(request, *args):
    page = request.GET.get('page')
    posts = Post.objects.all()
    sidebar = Category.objects.all()
    paginator = Paginator(posts, 3) #кількість постів, що відображаються на сторінці
    try:
        data_page = paginator.page(page)
    except PageNotAnInteger:
        data_page = paginator.page(1)
    except EmptyPage:
        data_page = paginator.page(paginator.num_pages)
    data_dict = {
        "posts": data_page,
        "sidebar": sidebar,
    }
    return render(request, 'blog_main.html', data_dict)#запит, адреса, словник із даними

@login_required
def profile(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, "Профіль оновлено")
            return redirect(to='user_profile')
    else:
        try:
            request.user.profile
        except Profile.DoesNotExist:
            Profile.objects.create(user = request.user).save()
        finally:
            profile_form = ProfileForm(instance=request.user.profile)
    profile = request.user.profile
    return render(request, 'profile.html',{
        'profile': profile,
        'profile_form': profile_form 
    })

def look_profile(request, username):
    look_for = Profile.objects.get(user__username=username) #у моделі user є модель username
    if look_for == request.user.profile:
        return redirect(to='user_profile')
    else:
        return render(request, "look_profile.html", {'profile': look_for})
    
def like_post(request, post_id):
    """"Add 1 like for 1 post per User"""
    post = Post.objects.get(id=post_id)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect(f'/{post.post_slug}')

def save_post(request, post_id):
    """"Save post"""
    post = Post.objects.get(id=post_id)
    if post.saving.filter(id=request.user.id).exists():
        post.saving.remove(request.user)
    else:
        post.saving.add(request.user)
    return redirect(f'/{post.post_slug}')

def show_saved(request):
    """"Functionality for profile to process saved form"""
    posts = Post.objects.filter(saving=request.user) 
    data_dict = { "posts": posts }
    return render(request, 'blog_main.html', data_dict)

def search_post(request):
    """Functionality for navbar to process search form"""
    posts = None
    if request.method == "POST":
        text = request.POST.get("searchpost")#отримуємо ім'я інпута із html-файла
        posts = Post.objects.filter(title__icontains=text) #шукаємо по полю title і lookup-пу icontains
    data_dict = { "posts": posts }
    return render(request, 'blog_main.html', data_dict)

def get_comment_form(request, post):
    """Post user commentary Form processing"""
    if request.method =="POST":
        form = AddCommentForm(request.POST)
        if form.is_valid():
            content = request.POST.get('content')
            comment = Comment.objects.create(post=post, author=request.user, content=content)
            comment.save()#зберігаємо об'єкт в базі данних
        return redirect(f'/{post.post_slug}')
    else:
        form = AddCommentForm()
    return form

def slug_process(request, slug):
    """Search URL in category slugs first and if no mathing
    Than searsh URL in post slugs
    In both cases show sidebar with categories"""
    sidebar = Category.objects.all()
    categories = [ c.category_slug for c in sidebar]
    if slug in categories:
        category_posts = Post.objects.filter(category__category_slug=slug)
        return render(request, "category.html", {
            "posts" : category_posts, 
            "sidebar": sidebar
        })

    post_slugs = [p.post_slug for p in Post.objects.all() ]
    if slug in post_slugs:
        post = Post.objects.get(post_slug = slug)
        if request.user.is_authenticated:
            if not post.views_number.filter(id=request.user.id).exists():
                #filter - повертає об'єкти, які відповідають певному параметру
                post.views_number.add(request.user)
        views = post.get_views_number()
        likes = post.get_likes_number()
        is_liked = post.likes.filter(id=request.user.id).exists()
        is_saved = post.saving.filter(id=request.user.id).exists()
        comments = Comment.objects.filter(post=post) #змінна=елементові класу post
        form = get_comment_form(request, post)
        data_dict = { 'post': post, 
                      'views_num': views,
                      'comment_form': form,
                      'comments': comments,
                      'likes_num': likes,
                      'is_liked': is_liked,
                      'is_saved': is_saved,
                      'sidebar': sidebar,
                    }
        return render(request, 'post_view.html', data_dict)

def register(request):
    #POST incoming
    if request.method == "POST":
        form = UserCreationForm(request.POST)#POST - словник зі всіма даними користувачі
        if form.is_valid():
            user = form.save()
            login(request, user)
            username = form.cleaned_data.get("username")
            messages.success(request, f"Створено новий акаунт: {username}")
            return redirect("/")
        else:
            print("ERROR DURING REGISTRATION!+")
            for msg in form.error_messages:
                messages.error(request, f"{msg}")
            return render(request, 'register.html', {'form': form})
    
    #GET incoming
    data_dict = {'form': UserCreationForm}
    return render(request, 'register.html', data_dict)

def logout_request(request):
    logout(request)
    messages.info(request ,"Ви вийшли з акаунту!")
    return redirect("/") 

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, "Ви упішно залогінились")
                return redirect("/")
            else:
                for msg in form.error_messages:
                    messages.error(request, f"Помилка, неправильний {msg}")
                return redirect("/login")
    form = AuthenticationForm()
    return render(request, "login.html", {'form': form})