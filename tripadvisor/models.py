# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from sorl.thumbnail import ImageField


class Photo(models.Model):
    image = ImageField(upload_to='photos')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.image.name

class Destination(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = _('Destination')
        verbose_name_plural = _('Destinations')

    def __str__(self):
        return self.name.encode('utf8')

class Link(models.Model):
    NATURE_PARKS = 'NATURE_PARKS'
    MUSEUMS = 'MUSEUMS'
    SHOPPING = 'SHOPPING'
    ZOOS_AQUARIUMS = 'ZOOS_AQUARIUMS'
    FOOD_DRINK = 'FOOD_DRINK'
    WATER_AMUSEMENT_PARKS = 'WATER_AMUSEMENT_PARKS'
    RESTAURANTS = 'RESTAURANTS'
    CATEGORY_CHOICES = (
        (NATURE_PARKS, 'Nature & Parks'),
        (MUSEUMS, 'Museums'),
        (SHOPPING, 'Shopping'),
        (ZOOS_AQUARIUMS, 'Zoos & Aquariums'),
        (FOOD_DRINK, 'Food & Drink'),
        (WATER_AMUSEMENT_PARKS, 'Water & Amusement Parks'),
        (RESTAURANTS, 'Restaurants'),
    )

    category = models.CharField(
        max_length=200,
        choices=CATEGORY_CHOICES,
        default=NATURE_PARKS,
    )
    destination = models.ForeignKey('Destination', on_delete=models.CASCADE)
    items_count = models.IntegerField(default=10)
    url = models.URLField()
    executed = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Link')
        verbose_name_plural = _('Links')

    def __str__(self):
        return self.url

class Listing(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=255)
    about = models.TextField(blank=True, null=True)
    link = models.ForeignKey('Link', on_delete=models.CASCADE)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    features = models.TextField(blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    price_from = models.CharField(max_length=255, blank=True, null=True)
    price_to = models.CharField(max_length=255, blank=True, null=True)
    lat = models.CharField(max_length=255, blank=True, null=True)
    lng = models.CharField(max_length=255, blank=True, null=True)

    about_ar = models.TextField(blank=True, null=True)
    title_ar = models.TextField(blank=True, null=True)
    features_ar = models.TextField(blank=True, null=True)

    photos = GenericRelation('Photo')

    class Meta:
        verbose_name = _('Listing')
        verbose_name_plural = _('Listings')

    def __str__(self):
        return self.title

class WorkingHours(models.Model):
    listing = models.ForeignKey('Listing', on_delete=models.CASCADE)
    day = models.CharField(max_length=125)
    time_from = models.CharField(max_length=125, blank=True)
    time_to = models.CharField(max_length=125, blank=True)

    class Meta:
        verbose_name = _('WorkingHour')
        verbose_name_plural = _('WorkingHours')

    def __str__(self):
        return self.day.encode('utf8')
