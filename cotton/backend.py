from ytmusicapi import YTMusic
from yt_dlp import YoutubeDL
from typing import List, Dict
import os

def search(query: str, filter_type: str) -> Dict:
    try:
        results = YTMusic().search(query, filter=filter_type)
        if not results:
            raise ValueError(f"query '{query}' yields no results")
        return results[0]
    except Exception as e:
        raise RuntimeError(f"search(): {str(e)}")

def get_release(result: Dict) -> Dict:
    try:
        browse_id = result["browseId"]
        release = YTMusic().get_album(browse_id)
        if not release:
            raise ValueError(f"no release found for browseId '{browse_id}'")
        return release
    except Exception as e:
        raise RuntimeError(f"get_release(): {str(e)}")

def get_artist(result: Dict) -> Dict:
    try:
        browse_id = result["browseId"]
        artist = YTMusic().get_artist(browse_id)
        if not artist:
            raise ValueError(f"no artist found for browseId '{browse_id}'")
        return artist
    except Exception as e:
        raise RuntimeError(f"get_artist(): {str(e)}")

def get_discography(artist: Dict) -> List[Dict]:
    try:
        releases = artist.get("albums", {}).get("results", []) + artist.get("singles", {}).get("results", [])
        discography = [get_release(release) for release in releases]
        return discography
    except Exception as e:
        raise RuntimeError(f"get_discography(): {str(e)}")

def download_release(release: Dict, path: str, ydl_opts: Dict) -> None:
    try:
        playlist_id = release["audioPlaylistId"]
        artist = release["artists"][0]["name"]
        title = release["title"]
        track_count = release["trackCount"]

        # Create path dir if it does not exist
        expanded_path = os.path.expanduser(path)
        os.makedirs(expanded_path, exist_ok=True)

        # Do not store singles in dedicated directories
        if track_count == 1:
            outtmpl = os.path.join(expanded_path, artist, "%(title)s.%(ext)s")
        else:
            outtmpl = os.path.join(expanded_path, artist, title, "%(title)s.%(ext)s")
        ydl_opts_copy = ydl_opts.copy()
        ydl_opts_copy["outtmpl"] = outtmpl

        with YoutubeDL(ydl_opts_copy) as ydl:
            ydl.download([f"https://music.youtube.com/playlist?list={playlist_id}"])
    except Exception as e:
        raise RuntimeError(f"download_release(): {str(e)}")
