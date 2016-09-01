from PIL import Image
import io
import json
import http.client


def get_image_list(movie_json: str) -> list:
    movies = json.loads(movie_json, encoding="utf-8")
    images = []
    for movie in movies:
        images.append({
            "name": movie["title"],
            "url": movie["image"]
        })
    return images


def download_images(image_list: list):
    conn = http.client.HTTPSConnection("img3.doubanio.com")
    for image_info in image_list:
        url = image_info["url"].split(".com")[1]
        conn.request("GET", url)
        response = conn.getresponse()
        image = Image.open(io.BytesIO(response.read()))
        size = (int(image.size[0] * 300 / image.size[1]), 300)
        image.thumbnail(size)
        image.save("img/%s.jpg" % image_info["name"], "JPEG")
        print("Download file: %s.jpg" % image_info["name"])


if __name__ == "__main__":
    movie_json = open("my_movie.json", "rt", encoding="utf-8").read()
    images = get_image_list(movie_json)
    download_images(images)