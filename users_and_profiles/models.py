from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.utils.translation import gettext_lazy as _
from PIL import Image


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=30, unique=True)
    profile_picture = models.ImageField(default='default.jpg', upload_to='profile_pictures')
    friends = models.ManyToManyField("Profile", blank=True)
    online = models.BooleanField(default=False)

    def __str__(self):
        return self.nickname

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.profile_picture.path)
        img_dimension = 300

        if img.height < img_dimension or img.width < img_dimension \
                or img.width == img.height:
            img_resized = img.resize((img_dimension, img_dimension), Image.Resampling.LANCZOS)
            img_resized.save(self.profile_picture.path)
        elif img.height > img_dimension or img.width > img_dimension:
            width, height = img.size

            left = (width - img_dimension) // 2
            top = (height - img_dimension) // 2
            right = (width + img_dimension) // 2
            bottom = (height + img_dimension) // 2

            img_cropped = img.crop((left, top, right, bottom))
            img_cropped.save(self.profile_picture.path)



class FriendRequest(models.Model):
    from_user = models.ForeignKey(Profile, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(Profile, related_name='to_user', on_delete=models.CASCADE)

    def __str__(self):
        return f"Friend request from {self.from_user} to {self.to_user}"
