import os
from collections import defaultdict
import subprocess
from os import PathLike
from typing import List
from progressbar import progressbar
import json
from hashlib import md5


class Image:
    def __init__(self, album: 'Album', exif):
        self.album = album
        self.path = exif['SourceFile']
        self.fname = os.path.basename(self.path)
        self.iso = exif['ISO']
        self.exposure = exif['ExposureTime']

    @property
    def thumbnail(self):
        return self.album.get_thumbnail_path(self)

    @property
    def thumb_basename(self):
        return self.album.get_thumbnail_basename(self)

class Album:
    def __init__(self, home: 'Library', path: PathLike, glob: str):
        self.home = home
        self.path = path
        self.glob = glob
        self.images: List[Image] = []
        self.unique_name = md5(self.path.encode()).hexdigest()

    def __getitem__(self, fname) -> Image:
        for image in self.images:
            if image.fname == fname:
                return image
        raise KeyError()

    def stats(self):
        by_iso = defaultdict(lambda: defaultdict(int))
        unique_exp = set()
        for image in self.images:
            by_iso[image.iso][image.exposure] += 1
            unique_exp.add(image.exposure)
        return unique_exp, by_iso

    @property
    def remote_glob(self):
        return os.path.join(self.path, self.glob)

    @property
    def exif_path(self):
        return os.path.join(self.home.exif_home, self.unique_name + ".json")

    @property
    def thumb_path(self):
        return os.path.join(self.home.thumb_home, self.unique_name)

    def get_thumbnail_path(self, image: Image):
        return os.path.join(self.thumb_path, self.get_thumbnail_basename(image))

    def get_thumbnail_basename(self, image: Image):
        return image.fname + "." + self.home.defaults['thumbnail']['ext']

class Library:
    def __init__(self, paths, albums, defaults):
        self.paths = paths
        self.albums = [Album(home=self, **cfg) for cfg in albums]
        self.defaults = defaults

        self._make_paths()
        for album in self.albums:
            self.load_exifs(album)

    def _make_paths(self):
        os.makedirs(self.paths['thumbs'], exist_ok=True)
        os.makedirs(self.paths['exifdb'], exist_ok=True)

    @property
    def exif_home(self):
        return self.paths['exifdb']

    @property
    def thumb_home(self):
        return self.paths['thumbs']

    @property
    def exif_tool(self):
        return self.defaults['exif']['tool']

    def load_exifs(self, album: Album):
        if not os.path.exists(album.exif_path):
            print("generating exifs")
            subprocess.run(f"{self.exif_tool} {album.remote_glob} -json > {album.exif_path}", shell=True, check=True)
        with open(album.exif_path) as fh:
            album.images = [Image(album, ex) for ex in json.load(fh)]
        print(f"loaded exifs for {album.unique_name}")

    def make_all_thumbnails(self, pbar=True):
        for album in self.albums:
            self.make_thumbnails(album, pbar=pbar)
            print(f"checked {len(album.images)} thumbnails for {album.unique_name}")

    def make_thumbnails(self, album: Album, pbar=True, overwrite=False):
        os.makedirs(album.thumb_path, exist_ok=True)
        for image in progressbar(album.images):
            if os.path.exists(image.thumbnail):
                print("thumbnail exists " + image.thumbnail)
                continue
            cp = subprocess.run([
                self.defaults['thumbnail']['tool'],
                image.path,
                "-thumbnail",
                self.defaults['thumbnail']['size'],
                image.thumbnail], check=False)

            if cp.returncode != 0:
                print(f"ERROR converting {image.path}")
            else:
                print("generated thumbnail " + image.thumbnail)

    def __getitem__(self, key: str) -> Album:
        for album in self.albums:
            if key == album.unique_name:
                return album
        raise KeyError()
