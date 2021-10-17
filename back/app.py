import os
from collections import defaultdict
import subprocess
from os import PathLike
from typing import List
from progressbar import progressbar
import json
from hashlib import md5

import yaml


class Image:
    def __init__(self, album: 'Album', exif):
        self.album = album
        self.path = exif['SourceFile']
        self.fname = os.path.basename(self.path)
        self.iso = exif['ISO']
        self.exposure = exif['ExposureTime']

    def detail(self):
        return {
            "path": self.path,
            "fname": self.fname,
            "iso": self.iso,
            "exposure": self.exposure,
            "thumbnail": self.thumb_basename,
            "ordinal": self.ordinal
        }

    @property
    def thumbnail(self):
        return self.album.get_thumbnail_path(self)

    @property
    def thumb_basename(self):
        return self.album.get_thumbnail_basename(self)

    @property
    def ordinal(self):
        return int(self.fname.split("_")[1].split(".")[0])

class Sequence:
    def __init__(self, name, start=None, end=None, extra=None):
        self.name = name
        self.start = start
        self.end = end
        self.extra: List[str] = extra if extra else []

    def __contains__(self, image: Image):
        if image.fname in self.extra:
            return True
        if self.start is not None and self.end is not None:
            try:
                if image.ordinal >= self.start and image.ordinal <= self.end:
                    return True
            except Exception as e:
                print(e)
                return False

class Album:
    def __init__(self, home: 'Library', path: PathLike, glob: str):
        self.home = home
        self.path = path
        self.glob = glob
        self.images: List[Image] = []
        self.unique_name = md5(self.path.encode()).hexdigest()
        self.notes = []
        self.sequences = []
        self.image_notes = {}

    def detail(self):
        return {
            "path": self.path,
            "glob": self.glob,
            "images": [img.fname for img in self.images],
            "unique_name": self.unique_name,
            "notes": self.notes,
            "sequences": [seq.name for seq in self.sequences],
            "image_notes": self.image_notes
        }

    def summary(self):
        return {
            "unique_name": self.unique_name,
            "path": self.path,
            "images": len(self.images),
            "note": self.notes[0] if self.notes else ""
        }

    def load_notes(self):
        if not os.path.exists(self.notes_path):
            print(f"notes not found for {self.unique_name}")
            return
        with open(self.notes_path) as fh:
            j = json.load(fh)
        self.notes = j.get('album_notes', [])
        self.sequences = [Sequence(**cfg) for cfg in j.get('sequences', [])]
        self.image_notes = j.get('image_notes', {})

    def get_sequences(self, image: Image):
        return [
            seq.name for seq in self.sequences if image in seq
        ]

    def save_notes(self):
        j = {
            'album_notes': self.notes,
            'sequences': self.sequences,
            'image_notes': self.image_notes
        }
        with open(self.notes_path, 'w') as fh:
            json.dump(j, fh)

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

    @property
    def notes_path(self):
        return os.path.join(self.home.notes_home, self.unique_name + ".json")

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
        os.makedirs(self.paths['notes'], exist_ok=True)

    @property
    def exif_home(self):
        return self.paths['exifdb']

    @property
    def thumb_home(self):
        return self.paths['thumbs']

    @property
    def notes_home(self):
        return self.paths['notes']

    @property
    def exif_tool(self):
        return self.defaults['exif']['tool']

    def load_exifs(self, album: Album, load_notes=True):
        if not os.path.exists(album.exif_path):
            print("generating exifs")
            subprocess.run(f"{self.exif_tool} {album.remote_glob} -json > {album.exif_path}", shell=True, check=True)
        with open(album.exif_path) as fh:
            album.images = [Image(album, ex) for ex in json.load(fh)]
        if load_notes:
            album.load_notes()
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

def get_config(path=None):
    if path:
        if not os.path.exists(path):
            raise Exception(f"Can't find config file {path}")
    else:
        path = "./config.yaml"
        if not os.path.exists(path):
            print("creating default config")
            os.link("./default_config.yaml", path)
    with open(path) as fh:
        return yaml.safe_load(fh)
