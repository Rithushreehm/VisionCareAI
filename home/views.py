from django.shortcuts import render
from .ai import analyze_product
import os


def home(request):
    return render(request, "home.html")


def result(request):

    if request.method == "POST":

        image = request.FILES["image"]

        os.makedirs("media", exist_ok=True)

        image_path = os.path.join("media", image.name)

        with open(image_path, "wb+") as f:
            for chunk in image.chunks():
                f.write(chunk)

        try:
            response = analyze_product(image_path)
        except Exception as e:
            response = f"Error: {e}"

        context = {
            "result": response,
            "image": "/" + image_path
        }

        return render(request, "result.html", context)

    return render(request, "home.html")