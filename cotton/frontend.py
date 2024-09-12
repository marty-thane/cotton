from cotton.backend import *
from tabulate import tabulate
from concurrent.futures import ThreadPoolExecutor
import argparse

def print_queue(queue: List[Dict]) -> None:
    print("\nYou are about to download the following releases:\n")

    table_data = []
    for release in queue:
        title = release["title"]
        artist = release["artists"][0]["name"]
        track_count = release["trackCount"]

        table_data.append([title, artist, track_count])

    headers = ["Title", "Artist", "Track Count"]
    print(tabulate(table_data, headers=headers), "\n")

def get_consent() -> bool:
    response = input("Proceed? [Y/n]: ").strip().lower()
    if response in ["y", "yes", ""]:
        return True
    else:
        return False

def download_queue(queue: List[Dict], path: str, ydl_opts: Dict) -> None:
    with ThreadPoolExecutor(max_workers=4) as executor:
        for release in queue:
            executor.submit(download_release, release, path, ydl_opts)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--codec", type=str, default="mp3", help="specify the file format to use (default: %(default)s)")
    parser.add_argument("--path", type=str, default=os.path.join("~", "Music"),
                        help="specify where to store files (default: %(default)s)")
    parser.add_argument("--yes", action="store_true", help="do not prompt the user for confirmation")
    parser.add_argument("scope", type=str, choices=["artist", "release"], help="select the scope in which to search")
    parser.add_argument("keyword", type=str, nargs="+", help="one or more keywords to search for")
    args = parser.parse_args()

    query = " ".join(args.keyword)
    scope_to_filter = {
            "artist": "artists",
            "release": "albums"
            }
    filter_type = scope_to_filter[args.scope]

    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "noprogress": True,
        "format": "bestaudio/best",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": args.codec,
        }],
    }

    try:
        result = search(query, filter_type)

        if filter_type == "artists":
            artist = get_artist(result)
            queue = get_discography(artist)
        else:
            release = get_release(result)
            queue = [release]
        print_queue(queue)

        if args.yes or get_consent():
            download_queue(queue, args.path, ydl_opts)
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
