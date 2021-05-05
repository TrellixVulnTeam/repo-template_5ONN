from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

import cloudinary
import cloudinary.uploader
import cloudinary.api

from cloudinary.forms import cl_init_js_callbacks

from .models import Photo
from .forms import PhotoForm


def portfolio(request):
    """ A view to show all portfolio items"""
    photos = Photo.objects.all().order_by('-date_time')

    context = {
        'photos': photos
    }
    template = 'portfolio/portfolio.html'

    return render(request, template, context)

@login_required
def upload_photo(request):

    if not request.user.is_superuser:
        sweetify.sweetalert(
            request, title='error', icon='error',
            text="This functionality is available to admin only.",
            timer=2000)
        return redirect(reverse('portfolio'))

    if request.method == 'POST':
        upload_form = PhotoForm(request.POST, request.FILES)
        if upload_form.is_valid():
            upload_form.save()
            messages.success(request, 'Successfully added product!')
            return redirect('portfolio')
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid.') 

    else:
        upload_form = PhotoForm()

    template = 'portfolio/upload-photo.html'
    context = {
        'upload_form': upload_form
    }
    return render(request, template, context)