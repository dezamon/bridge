# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
import re

from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, _user_has_perm
)
from django.core import validators
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings

# The below code is triggered whenever a new user has been created and saved to DB
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

# PLAN
ACCOUNT_TYPE = (
    ('client','Client'),
    ('designer','Designer'),
)

class UserManager(BaseUserManager):
    def create_user(self, username, email, password, **extra_fields):
        """ Creates and saves User with the given email and password. """
        now = timezone.now()
        if not email:
            raise ValueError('Users must have an email address.')
        email = UserManager.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            is_active=False,
            last_login=now,
            date_joined=now,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        """ Creates and saves a superuser with the given email and password. """
        user = self.create_user(username, email, password)
        user.is_active = True
        user.is_staff = True
        user.is_admin = True
        # user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    """User """
    username    = models.CharField(_('username'),
                                   max_length=30,
                                   unique=False,
                                   help_text=_('Required. 30 characters or fewer. Letters, numbers and '
                                   '@/./+/-/_ characters'))
    first_name  = models.CharField(_('first name'), max_length=30, blank=True)
    last_name   = models.CharField(_('last name'), max_length=30, blank=True)
    email       = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    is_active   = models.BooleanField(default=False)
    is_staff    = models.BooleanField(default=False)
    is_admin    = models.BooleanField(default=False)
    is_suspend  = models.BooleanField(default=False)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    delete      = models.BooleanField(default=False)
    account     = models.CharField(choices=ACCOUNT_TYPE, max_length=10, default="", blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def user_has_perm(user, perm, obj):
        """
        A backend can raise `PermissionDenied` to short-circuit permission checking.
        """
        return _user_has_perm(user, perm, obj)

    def has_perm(self, perm, obj=None):
        return _user_has_perm(self, perm, obj=obj)

    def has_module_perms(self, app_label):
        return self.is_admin

    def get_short_name(self):
        return self.first_name

    def __unicode__(self):
        return u'{0}'.format(self.username)

    def __str__(self):
        return u'{0}'.format(self.username)

    @property
    def is_superuser(self):
        return self.is_admin

class PasswordReset(models.Model):
    email = models.EmailField(max_length=255, unique=True)
    access_key = models.CharField(max_length=100)

    def __str__(self):
        return u'{0}'.format(self.email)
