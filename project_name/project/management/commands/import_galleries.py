import time
import os.path

from datetime import datetime
from pprint import pprint

from django.core.management.base import BaseCommand, CommandError

from django.utils import simplejson as json

from photologue.models import Gallery, Photo


class Command(BaseCommand):
    args = '<galleries_filename> <pictures_filename> - path to json files'
    help = 'Imports data nggalleries json to Django Photologue'
    
    def handle(self, *args, **options):
        if len(args) != 2:
            raise CommandError("This command takes exactly two arguments")
        galleries_filename, pictures_filename = args
        with open(galleries_filename, 'r') as gh:
            galleries = json.load(gh)


        galleries_result = {}
        paths = {} 

        for gallery in galleries:
            paths[gallery['gid']] = gallery['path']
            kwargs = {
                'title': gallery['title'],
                'title_slug': gallery['slug'],
                'description': gallery['galdesc'],
            }
            try:
                new_gallery = Gallery.objects.get(title_slug=gallery['slug'])
                for key, value in kwargs.items():
                    setattr(new_gallery, key, value)
            except Gallery.DoesNotExist:
                new_gallery = Gallery(**kwargs)
            new_gallery.save()
            galleries_result[gallery['gid']] = new_gallery

        with open(pictures_filename, 'r') as ph:
            pictures = json.load(ph)

        result = []
        for picture in pictures:
            path = paths[picture['galleryid']]
            kwargs = {
                'title': picture['alttext'],
                'title_slug': picture['image_slug'],
                'date_taken': datetime(*time.strptime(picture['imagedate'], "%Y-%m-%d %H:%M:%S")[0:6]),
                'image': os.path.join('/'.join(path.split('/')[1:]), picture['filename']),
                'caption': picture['description'],
                'is_public': not bool(picture['exclude']),
            }
            d = 0
            try:
                new_photo = Photo.objects.get(title_slug=picture['image_slug'])
                for key, value in kwargs.items():
                    setattr(new_gallery, key, value)
            except Photo.DoesNotExist:
                new_photo = Photo(**kwargs)
                while True:
                    try:
                        if d:
                            title = new_photo.title + (' %d' % d)
                        else:
                            title = new_photo.title
                        Photo.objects.get(title=title)
                        d+=1
                    except Photo.DoesNotExist:
                        new_photo.title = title
                        break
            gallery = galleries_result[picture['galleryid']]
            new_photo.save()
            gallery.photos.add(new_photo)
