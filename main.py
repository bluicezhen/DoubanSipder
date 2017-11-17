from func import get_movie_info, get_movie_url_list


def main(douban_username: str):
    movie_list = get_movie_url_list(douban_username)

    res_year_dict = {}

    for movie in movie_list:
        movie_info = get_movie_info(movie["url"])
        if movie_info["year"] not in res_year_dict:
            res_year_dict[movie_info["year"]] = []
        res_year_dict[movie_info["year"]].append(movie["mark"])

    # Analyze "Year"
    for year, mark_list in res_year_dict.items():
        res_year_dict[year] = round(sum(mark_list) / len(mark_list), 1)
    # sorted(res_year_dict.items(), key=lambda asd: asd[1], reverse=True)

    # Out "Favorite Year"
    print("Your favorite year, top 10:")
    for year, mark in sorted(res_year_dict.items(), key=lambda asd: asd[1], reverse=True):
        print(f"\t{ mark } points: \t{ year }")


if __name__ == "__main__":
    main("bluicezhen")
