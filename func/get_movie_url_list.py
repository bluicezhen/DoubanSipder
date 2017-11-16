import requests
from bs4 import BeautifulSoup
from typing import List


def get_movie_url_list(douban_username: str) -> List[str]:
    start = 0
    movie_href_list = []

    while True:
        url = f"https://movie.douban.com/people/{ douban_username }/collect?" \
              f"start={ start }&sort=time&rating=all&filter=all&mode=list"
        res = requests.get(url)
        start += 30

        soup = BeautifulSoup(res.text, "html.parser")
        e_movie_href_list_in_page = soup.find_all("li", {"class": "item"})

        if len(e_movie_href_list_in_page) == 0:
            print("Complete: get movie list.")
            break

        for e_movie_href_in_page in e_movie_href_list_in_page:
            e_a = e_movie_href_in_page.find("a")
            movie_href_list.append(e_a.attrs["href"])
        print(f"Found: { len(movie_href_list) } movies.")

    return movie_href_list


if __name__ == "__main__":
    get_movie_url_list("bluicezhen")
