from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import ImageForm
from .models import Image
from testing import analyseImage
import numpy as np
from django.shortcuts import render, get_object_or_404


def home(request):
    return HttpResponse("Hello, world!")

# def upload_image(request):
#     if request.method == 'POST':
#         form = ImageForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('image_list')
#     else:
#         form = ImageForm()
#     return render(request, 'upload_image.html', {'form': form})

def image_list(request):
    images = Image.objects.all()
    return render(request, 'image_list.html', {'images': images})


def process_image(img):
    image_path = img.image.path
    result = analyseImage.analyze_urine_strip(image_path)
    result = [item.tolist() if isinstance(item, np.ndarray) else item for item in result]
    result_dict = {
        'URO': result[0],
        'BIL': result[1],
        'KET': result[2],
        'BLD': result[3],
        'PRO': result[4],
        'NIT': result[5],
        'LEU': result[6],
        'GLU': result[7],
        'SG': result[8],
        'PH': result[9],
    }

    img.result = result_dict
    img.save()

    return result_dict

def upload_image(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image_instance = form.save()
            result = process_image(image_instance)
            return render(request, 'upload_image.html', {'form': form, 'result': result})
    else:
        form = ImageForm()
    return render(request, 'upload_image.html', {'form': form})

def image_result(request):
    if request.method == 'POST':
        image_name = request.POST.get('image_name')  
        image = get_object_or_404(Image, title=image_name)  
        return render(request, 'image_result.html', {'image': image})
    return render(request, 'image_input.html')