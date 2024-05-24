from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Image
from .serializers import ImageSerializer
from .forms import ImageForm , ImageReq
from .analyseImage import analyze_urine_strip
import logging
import numpy as np
from django.http import HttpResponse
import os

logger = logging.getLogger(__name__)

@api_view(['POST'])
def upload_and_process_image(request):
    form = ImageForm(request.POST, request.FILES)
    if form.is_valid():
        try:
            image_instance = form.save()
            image_path = image_instance.image.path
            result = analyze_urine_strip(image_path)
            print(result)
            result_dict = {key: value.tolist() if isinstance(value, np.ndarray) else value for key, value in result.items()}
            image_instance.result = result_dict
            image_instance.save()
            return Response({'image_id': image_instance.id, 'title': image_instance.title, 'result': result_dict}, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.exception('err')
            return Response({"error": "err"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        logger.error('Form is not valid: %s', form.errors)
        return Response({"error": "Invalid form data"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def display_image_result(request, image_id):
    image_instance = get_object_or_404(Image, id=image_id)
    serializer = ImageSerializer(image_instance)
    return Response(serializer.data)

#get list of all patients/users who have entered the image of urine strip
@api_view(['GET'])
def list_all_image_titles(request):
    try:
        images = Image.objects.all()
        titles = [image.title for image in images]
        return Response(titles)
    except Exception as e:
        return Response({"error": "An internal error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#get the imageName from user and show results
@api_view(['GET'])
def getFromName(request, imageName):
    res = get_object_or_404(Image, title=imageName)
    serializer = ImageSerializer(res)
    return Response(serializer.data)

@api_view(['POST'])  
def postImageName(request):
    imageName = request.data.get('image_title', None)
    if imageName:
        form = ImageReq({'title': imageName})
        if form.is_valid():
            return Response({'image_title': imageName})
    return Response({'error': 'Invalid data provided'}, status=status.HTTP_400_BAD_REQUEST)

import json
#download the json result
@api_view(['GET'])
def downloadResult(request, imageId):
    try:
        res = Image.objects.get(id=imageId)  #id use
        resultData1 = res.result
        resultData = json.dumps(resultData1, indent=4)
        filePath = os.path.join('results', f'result_{imageId}.json')
        os.makedirs(os.path.dirname(filePath), exist_ok=True)
        with open(filePath, 'w') as file:
            file.write(str(resultData))
        with open(filePath, 'rb') as file:
            response = HttpResponse(file.read(), content_type='JSON')
            response['Content-Disposition'] = f'attachment; filename=result_{imageId}.json'
            return response

    except Image.DoesNotExist:
        return HttpResponse(status=404)





























































# THE ONE TO USE WITH HTML

# from django.shortcuts import render
# from django.http import HttpResponse
# from django.shortcuts import render, redirect
# from .forms import ImageForm
# from .models import Image
# from testing import analyseImage
# import numpy as np
# from django.shortcuts import render, get_object_or_404


# def home(request):
#     return HttpResponse("Hello, world!")

# # def upload_image(request):
# #     if request.method == 'POST':
# #         form = ImageForm(request.POST, request.FILES)
# #         if form.is_valid():
# #             form.save()
# #             return redirect('image_list')
# #     else:
# #         form = ImageForm()
# #     return render(request, 'upload_image.html', {'form': form})

# def image_list(request):
#     images = Image.objects.all()
#     return render(request, 'image_list.html', {'images': images})


# def process_image(img):
#     image_path = img.image.path
#     result = analyseImage.analyze_urine_strip(image_path)
#     result = [item.tolist() if isinstance(item, np.ndarray) else item for item in result]
#     result_dict = {
#         'URO': result[0],
#         'BIL': result[1],
#         'KET': result[2],
#         'BLD': result[3],
#         'PRO': result[4],
#         'NIT': result[5],
#         'LEU': result[6],
#         'GLU': result[7],
#         'SG': result[8],
#         'PH': result[9],
#     }

#     img.result = result_dict
#     img.save()

#     return result_dict

# def upload_image(request):
#     if request.method == 'POST':
#         form = ImageForm(request.POST, request.FILES)
#         if form.is_valid():
#             image_instance = form.save()
#             result = process_image(image_instance)
#             return render(request, 'upload_image.html', {'form': form, 'result': result})
#     else:
#         form = ImageForm()
#     return render(request, 'upload_image.html', {'form': form})

# def image_result(request):
#     if request.method == 'POST':
#         image_name = request.POST.get('image_name')  
#         image = get_object_or_404(Image, title=image_name)  
#         return render(request, 'image_result.html', {'image': image})
#     return render(request, 'image_input.html')