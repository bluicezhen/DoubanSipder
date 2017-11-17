import requests
from bs4 import BeautifulSoup


def get_movie_info(url: str):
    # res = requests.get(url)
    res = requests.get(url,
                       proxies={'http': 'http://127.0.0.1:8888', 'https': 'http://127.0.0.1:8888'},
                       verify=False)
    soup = BeautifulSoup(res.text, "html.parser")
    movie = {}

    # Get movie name
    movie["name"] = soup.find("span", {"property": "v:itemreviewed"}).text
    print("Analyze:", movie["name"])

    # Get movie release year
    movie["year"] = soup.find("span", {"class": "year"}).text[1:5]

    # Get Movie director
    e_director_list = soup.find_all("a", {"rel": "v:directedBy"})
    movie["director"] = []
    for e_director in e_director_list:
        movie["director"].append({"name": e_director.text, "url": e_director.attrs["href"]})

    # Get movie actor
    e_actor_list = soup.find_all("a", {"rel": "v:starring"})
    movie["actor"] = []
    for e_actor in e_actor_list:
        movie["actor"].append({"name": e_actor.text, "url": e_actor.attrs["href"]})
    movie["actor"] = movie["actor"][0:7]

    return movie


if __name__ == "__main__":
    import json

    print(json.dumps(get_movie_info("https://movie.douban.com/subject/1291843/"), indent=4, ensure_ascii=False))
