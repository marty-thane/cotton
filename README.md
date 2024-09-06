Cotton
======
Cotton is a music downloader for people who know what they want. It allows you
to fetch individual albums/singles or entire discographies with a single
command and store them in a sane directory structure, so chaos does not reign
over your library.

Installation
------------
Cotton can be installed via `pip`. To do this, open the terminal and run the
following commands:

    git clone https://github.com/marty-thane/cotton
    cd cotton/
    pip install .

**Note:** Cotton depends on [ffmpeg](https://www.ffmpeg.org/) for file format
conversion. Ensure it is installed prior to running.

Usage
-----
Reading the help documentation is the first step in understanding any program:

    usage: frontend.py [-h] [--codec CODEC] [--path PATH] [--yes] {artist,release} keyword [keyword ...]

    positional arguments:
      {artist,release}  select the scope in which to search
      keyword           one or more keywords to search for

    options:
      -h, --help        show this help message and exit
      --codec CODEC     specify the file format to use (default: mp3)
      --path PATH       specify where to store files (default: ~/Music)
      --yes             do not prompt the user for confirmation


A basic usage example might look like this:

    cotton release bold as love hendrix

If you already have a list of artists stored in a file, you can do the
following in your terminal:

    while read artist; do
        cotton --yes artist $artist
    done < artist_list.txt

Technical Notes
---------------
Cotton relies on `ytmusicapi` for searching and `yt_dlp` for downloading music.
Internally, it is split into two submodules: frontend and backend.
