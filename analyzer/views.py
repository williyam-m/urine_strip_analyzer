import cv2
import numpy as np
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser


@api_view(['POST'])
def upload_image(request):

    if 'image' not in request.FILES:
        return JsonResponse({'error': 'No image uploaded'}, status=400)

    file = request.FILES['image']
    image = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(image, cv2.IMREAD_COLOR)


    colors = extract_colors(img)

    return JsonResponse(colors)


def upload_page(request):
    return render(request, 'upload.html')


def extract_colors(img):
    try:
        # image -> RGB
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


        height, width, _ = img_rgb.shape
        strip_width = width // 10

        # to store the colors
        colors = []

        for i in range(10):
            x_start = i * strip_width
            x_end = (i + 1) * strip_width
            roi = img_rgb[:, x_start:x_end]

            avg_color_per_row = np.average(roi, axis=0)
            avg_color = np.average(avg_color_per_row, axis=0)

            avg_color = avg_color.astype(int).tolist()
            colors.append(avg_color)

        color_dict = {
            'URO': colors[0],
            'BIL': colors[1],
            'KET': colors[2],
            'BLD': colors[3],
            'PRO': colors[4],
            'NIT': colors[5],
            'LEU': colors[6],
            'GLU': colors[7],
            'SG': colors[8],
            'PH': colors[9]
        }

        return color_dict
    except Exception as e:

        print(f"Error in extract_colors: {e}")
        return {'error': str(e)}