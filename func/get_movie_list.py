import requests
from bs4 import BeautifulSoup


def get_movie_list():
    start = 0
    movie_href_list = []

    while True:
        url = f"https://movie.douban.com/people/bluicezhen/collect?" \
              f"start={ start }&sort=time&rating=all&filter=all&mode=list"
        res = requests.get(url,
                           proxies={"http": "http://127.0.0.1:8888", "https": "http://127.0.0.1:8888"},
                           verify=False)
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

    print(len(movie_href_list))


if __name__ == "__main__":
    get_movie_list()
