from django.db import models
from django.utils import timezone
from PIL import Image #pillow - бібліотека для роботи із зображеннями
from django.contrib.auth.models import User

#makemigrations - створює інструкції для додавання нової таблиці в базу даних
#migrate - виконує ці інструкції

#Post - публікація. кожен ряд в таблиці - відомості про 1 публікацію
    #кожна його властивість - колонка у таблиці, котра теж назвивається Post 

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='blog/static/img/profiles',
                               default = 'blog/static/img/profiles/default.png',
                               verbose_name = 'Фото профілю')
    about = models.TextField(max_length=500,
                             verbose_name = 'Про себе',
                             blank=True)
    def save(self,*agr, **kwargs):
        super().save()
        img = Image.open(self.avatar.path)
        if img.height>120 or img.width>120:
            img.thumbnail((120, 120))
            img.save(self.avatar.path)
    def __str__(self):
        return self.user.username

class Category(models.Model):
    name = models.CharField(max_length=80)
    info = models.TextField(blank=True)
    category_slug = models.CharField(max_length=80, default="category_main")
    img = models.ImageField(upload_to='blog/static/img/categories',
                            height_field=None,
                            width_field=None,
                            verbose_name="Зображення категорії", 
                            default='default.jpg')
    class Meta:
        verbose_name_plural = "Категорії"
    def save(self,*agr, **kwargs):
        super().save()
        img = Image.open(self.img.path)
        if img.height>200 or img.width>200:
            img.thumbnail((200, 200))
            img.save(self.img.path)
    def __str__(self):
        return f"{self.name}   URL: {self.category_slug}"

class Post(models.Model): 
    title = models.CharField(max_length=100) #CharField - тип для короткого тексту
    text = models.TextField() #для зберігання тексту
    created_at = models.DateField(default=timezone.now) #час коли таблиця створена
    post_slug = models.SlugField(max_length=80, default="default_post") #коротка назва поста для url
    img = models.ImageField(default = 'blog/static/img/default.jpeg', 
                            upload_to='blog/static/img', 
                            height_field=None, width_field=None,
                            max_length=200,
                            verbose_name="Картинка для поста") #поле для зображення
    views_number = models.ManyToManyField(User, related_name="views_rating", blank=True)
    likes = models.ManyToManyField(User, related_name="post_likes", blank=True)
    saving =  models.ManyToManyField(User, related_name="post_savings", blank=True)
    category = models.ForeignKey(Category, default=1, 
                                 on_delete=models.SET_DEFAULT,
                                 verbose_name="Категорія")
    def get_views_number(self):
        return self.views_number.count()
        #upload_to='' - папка для завантаження
        #static -  статичні файли 
        #max_length=200 - максимальна довжина посилання на зображення
    def get_likes_number(self):
        return self.likes.count()
    def save(self, *arg, **kwargs): #ф-ція для збереження картинок на сайт, < зображення
        super().save() #збереження для класу models
        img = Image.open(self.img.path) #шлях зображення
        if img.height > 720 or img.width > 1080:
            img.thumbnail((720, 1080))
            img.save(self.img.path)
    def __str__(self): #при викликанні print буде повертатися саме заголовок(title)
        return self.title

    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments",)
    #.CASCADE - каскадне видалення коментарів при видаленні поста
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateField(default=timezone.now)
    def __str__(self): 
        return self.content
