from func import get_movie_url_list


def main(douban_username: str):
    movie_url_list = get_movie_url_list(douban_username)
    for movie_url in movie_url_list:
        print(movie_url)


if __name__ == "__main__":
    main("bluicezhen")
