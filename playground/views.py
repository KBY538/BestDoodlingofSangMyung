import base64
import os
import numpy as np
import cv2
from django.http import JsonResponse

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from doodling.settings import MEDIA_ROOT, STATIC_URL, BASE_DIR
from playground.spade.generate import evaluate

# Create your views here.


@csrf_exempt
def playground(request):
    if request.method == "POST":
        data = request.POST.get('data')
        data = data[22:]
        path = MEDIA_ROOT + '/segmentationImage/'
        number = len(os.listdir(path)) + 1

        filename = path + 'label' + str(number) + '.png'

        image = open(filename, "wb")
        image.write(base64.b64decode(data))
        image.close()

        generated_img_file = generate_image(filename)
        generated_img = cv2.imread(generated_img_file)
        generated_img_size_up = size_up(generated_img)

        cv2.imwrite(generated_img_file, generated_img_size_up)

        generated_img_file = generated_img_file.replace(BASE_DIR, '')
        generated_img_file = generated_img_file.replace('_', '')

        return JsonResponse({"filename": generated_img_file})

    else:
        return render(
            request,
            'playground/make_doodle.html'
        )


def size_up(img):
    sr = cv2.dnn_superres.DnnSuperResImpl_create()
    sr.readModel(BASE_DIR+STATIC_URL+'playground/superresolution/EDSR_x4.pb')
    sr.setModel("edsr", 4)
    result = sr.upsample(img)
    return result


def generate_image(filepath):
    img = cv2.imread(filepath)
    label = label_maker(img)
    return evaluate(label)


colors = {5: [250, 206, 135],  # 하늘
          2: [144, 238, 144],  # 앞산
          1: [170, 178, 32],  # 뒷산
          6: [0, 165, 255],  # 땅
          7: [153, 136, 119],  # 바위
          8: [128, 128, 240],  # 풀
          9: [225, 105, 65],  # 물
          4: [19, 69, 139],  # 가까운 나무
          3: [143, 143, 188],  # 먼 나무
          0: [0, 0, 0]  # None
          }


def distance(x1, x2):
    dist = 0
    for d in range(len(x1)):
        dist += (x1[d] - x2[d]) ** 2
    return dist


def label_maker(img):
    label = np.zeros((256, 256))
    img = cv2.resize(img, (256, 256), cv2.INTER_NEAREST)

    values, _ = np.unique(img.reshape((-1, 3)), axis=0, return_counts=True)
    curr_colors = [c for c in values.tolist() if c in colors.values()]

    for i in range(256):
        for j in range(256):
            if list(img[i][j]) in curr_colors:
                idx = curr_colors.index(list(img[i][j]))
                val = [k for k, v in colors.items() if v == curr_colors[idx]][0]
            else:
                min_dist = float('inf')
                val = colors[0]
                for c in curr_colors:
                    dist = distance(img[i][j], c)
                    if min_dist > dist:
                        min_dist = dist
                        val = [k for k, v in colors.items() if v == curr_colors[idx]][0]
                if min_dist == float('inf'):
                    val = 0
            label[i][j] = val
    label = label.astype(int)
    return label
