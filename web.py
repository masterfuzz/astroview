import sys
import os
import bottle
from bottle import route
import yaml
import app

lib: app.Library = {}

def main():
    global lib
    # with open(os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), "/config.yaml")) as fh:
    with open("./config.yaml") as fh:
        lib = app.Library(**yaml.safe_load(fh))
    lib.make_all_thumbnails()

    bottle.run(debug=True)

@route("/")
def index():
    return bottle.template("index.htm", albums=lib.albums)

@route("/albums/<album_id>")
def album(album_id):
    album = lib[album_id]
    unique_exp, by_iso = album.stats()
    return bottle.template("album.htm", album=album, unique_exp=unique_exp, by_iso=by_iso)
 
@route("/thumbs/<album_id>/<fname>")
def thumb(album_id, fname):
    album = lib[album_id]
    image = album[fname]
    return bottle.static_file(image.thumb_basename, root=album.thumb_path)

if __name__ == "__main__":
    main()

