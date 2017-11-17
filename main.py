from func import get_movie_info, get_movie_url_list


def main(douban_username: str):
    movie_list = get_movie_url_list(douban_username)

    res_year_dict = {}
    res_director_dict = {}
    res_actor_dict = {}

    i = 0
    for movie in movie_list:
        i += 1
        print(f"[{ round(i / len(movie_list) * 100, 1)}%]")
        movie_info = get_movie_info(movie["url"])

        # Year
        if movie_info["year"] not in res_year_dict:
            res_year_dict[movie_info["year"]] = []
        res_year_dict[movie_info["year"]].append(movie["mark"])

        # Director
        for director in movie_info["director"]:
            if director["name"] not in res_director_dict:
                res_director_dict[director["name"]] = []
            res_director_dict[director["name"]].append(movie["mark"])

        # Actor
        for actor in movie_info["actor"]:
            if actor["name"] not in res_actor_dict:
                res_actor_dict[actor["name"]] = []
            res_actor_dict[actor["name"]].append(movie["mark"])

    # Analyze "Year"
    for year, mark_list in res_year_dict.items():
        res_year_dict[year] = round(sum(mark_list) / len(mark_list), 1)

    # Analyze "Director"
    for director, mark_list in res_director_dict.items():
        res_director_dict[director] = round(sum(mark_list) / len(mark_list), 1)

    # Analyze "Actor"
    for actor, mark_list in res_actor_dict.items():
        res_actor_dict[actor] = round(sum(mark_list) / len(mark_list), 1)

    # Analyze "Director"

    # Out "Favorite Year"
    print("Your favorite year:")
    for year, mark in sorted(res_year_dict.items(), key=lambda asd: asd[1], reverse=True):
        print(f"\t{ mark } points: \t{ year }")

    # Out "Favorite Director"
    print("\nYour favorite director:")
    for director, mark in sorted(res_director_dict.items(), key=lambda asd: asd[1], reverse=True):
        print(f"\t{ mark } points: \t{ director }")

    # Out "Favorite Actor"
    print("\nYour favorite actor:")
    for actor, mark in sorted(res_actor_dict.items(), key=lambda asd: asd[1], reverse=True):
        print(f"\t{ mark } points: \t{ actor }")


if __name__ == "__main__":
    main("bluicezhen")
