import http.client
import time
from pprint import pprint
from bs4 import BeautifulSoup

DOUBAN_ID =         "bluicezhen"
USER_AGENT =        "Spider-37"
COMMON_HEADERS =    {
    "User-Agent": "Spider-37",
    "Connection": "keep-alive"
}

if __name__ == '__main__':
    def spider_movie():
        # Connect to 豆瓣电影.
        movie_connection = http.client.HTTPSConnection("movie.douban.com")

        # Get user movie page.
        movie_url = "/people/%s/" % DOUBAN_ID
        movie_connection.request("GET", movie_url, headers=COMMON_HEADERS)
        movie_response = movie_connection.getresponse()
        movie_html = movie_response.read().decode("utf-8")

        # Analysis user movie information
        movie_soup = BeautifulSoup(movie_html, "html.parser").find("div", {"id": "db-movie-mine"})
        movie_number_watched = int(movie_soup.find("h2").find("a").text.split("部")[0])

        # Get user movies which is watched.
        for i in range(0, movie_number_watched, 15):
            url = "https://movie.douban.com/people/%s/collect?start=%d&sort=time&rating=all&filter=all&mode=grid"\
                  % (DOUBAN_ID, i)
            try:
                movie_connection.request("GET", url, headers=COMMON_HEADERS)
                movies_page_response = movie_connection.getresponse()
            except http.client.ResponseNotReady:
                movie_connection = http.client.HTTPSConnection("movie.douban.com")
                movie_connection.request("GET", url, headers=COMMON_HEADERS)
                movies_page_response = movie_connection.getresponse()
            print("Get movie infomation page %d:" % (i / 15 + 1))
            movies_html = movies_page_response.read()

            # Find movies in page i.
            movies_soup = BeautifulSoup(movies_html, "html.parser").find("div", attrs={"class": "grid-view"})\
                .find_all("div", attrs={"class": "item"})

            for ms in movies_soup:
                title = ms.find("em").text.split(" ", 1)[0]
                date = ms.find("span", attrs={"class": "date"}).text
                score = 0
                for j in range(5, 0, -1):
                    score_html = ms.find("span", attrs={"class": "rating%d-t" % j})
                    if score_html is not None:
                        score = j
                        break
                try:
                    comment = ms.find("span", attrs={"class": "comment"}).text
                except AttributeError:
                    comment = ""
                link = ms.find("a").attrs["href"]
                image = "https://img3.doubanio.com/view/photo/photo/public/%s"\
                        % ms.find("img").attrs["src"].split("/public/")[1]

                print("\n\tFind movie\n\t\ttitle:   %s\n\t\tdate:    %s\n\t\tscore:   %d\n\t\tcomment: %s"
                      "\n\t\tlink:    %s\n\t\timage:   %s"
                      % (title, date, score, comment, link, image))

            if i == 0:     # Just for test
                break       # Just for test

            time.sleep(3)


if __name__ == "__main__":
    spider_movie()