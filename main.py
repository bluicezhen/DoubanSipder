import click
from func_init import init
from func_spider_movie import movie_get, movie_poster_download, movie_upload, movie_compile_to_html

COMMON_HEADERS = {
    "User-Agent": "Spider-37",
    "Connection": "keep-alive"
}


@click.group()
def main():
    pass

if __name__ == "__main__":
    main.add_command(init)
    main.add_command(movie_get)
    main.add_command(movie_poster_download)
    main.add_command(movie_upload)
    main.add_command(movie_compile_to_html)
    main()
