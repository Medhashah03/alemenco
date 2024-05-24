from django.urls import path
from .views import upload_and_process_image, display_image_result , list_all_image_titles,getFromName , postImageName ,downloadResult

urlpatterns = [
    path('api/upload_image/', upload_and_process_image, name='upload_and_process_image'),
    path('api/display_image_result/<int:image_id>/', display_image_result, name='display_image_result'),
    path('api/image_titles/', list_all_image_titles, name='list_all_image_titles'),
    path('api/get-result/<imageName>/', getFromName, name='getFromName'),
    path('api/imageName/', postImageName, name='postImageName'),
    path('api/download-result/<int:imageId>/', downloadResult, name='downloadResult'),
]

