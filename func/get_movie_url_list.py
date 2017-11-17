import requests
from bs4 import BeautifulSoup
from typing import Any, Dict, List


def get_movie_url_list(douban_username: str) -> List[Dict[str, Any]]:
    start = 0
    movie_href_list = []

    while True:
        url = f"https://movie.douban.com/people/{ douban_username }/collect?" \
              f"start={ start }&sort=time&rating=all&filter=all&mode=list"
        # res = requests.get(url,
        # proxies={'http': 'http://127.0.0.1:8888', 'https': 'http://127.0.0.1:8888'}
        # , verify=False)
        res = requests.get(url)
        start += 30

        soup = BeautifulSoup(res.text, "html.parser")
        e_movie_href_list_in_page = soup.find_all("li", {"class": "item"})

        if len(e_movie_href_list_in_page) == 0:
            print("Complete: get movie list.")
            break

        for e_movie_href_in_page in e_movie_href_list_in_page:
            try:
                movie_href_list.append({
                    "url": e_movie_href_in_page.find("a").attrs["href"],
                    "mark": int(
                        e_movie_href_in_page.find("div", {"class": "date"}).find("span").attrs["class"][0][6]) * 2
                })
            except AttributeError:
                print("You did not mark this movie:",
                      e_movie_href_in_page.find("a").text.replace('\n', "").replace(' ', ""),
                      e_movie_href_in_page.find("a").attrs["href"])

        print(f"Found: { len(movie_href_list) } movies.")

        # break

    return movie_href_list


if __name__ == "__main__":
    import json

    print(json.dumps(get_movie_url_list("bluicezhen"), ensure_ascii=False, indent=4))
