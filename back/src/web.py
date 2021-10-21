import bottle
from bottle import route, request
import app

lib: app.Library = {}

def main():
    global lib
    # with open(os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), "/config.yaml")) as fh:
    lib = app.Library(**app.get_config())
    lib.make_all_thumbnails()

    bottle.run(debug=True)

@route("/bottleui/")
def index():
    return bottle.template("index.htm", albums=lib.albums)

@route("/bottleui/albums/<album_id>")
def uialbum(album_id):
    album = lib[album_id]
    unique_exp, by_iso = album.stats()
    return bottle.template("album.htm", album=album, unique_exp=unique_exp, by_iso=by_iso)

@route("/api/albums")
def albums():
    return {
        "albums": [alb.summary() for alb in lib.albums]
    }

@route("/api/albums/<album_id>")
def album(album_id):
    album = lib[album_id]
    return album.detail()
    
@route("/api/albums/<album_id>/stats")
def album_stats(album_id):
    album = lib[album_id]
    unique_exp, by_iso = album.stats()
    return {
        "exposures": list(unique_exp),
        "exp_by_iso": by_iso
    }

@route("/api/albums/<album_id>/images")
def images(album_id):
    album = lib[album_id]
    return {
        "images": [img.detail() for img in album.images]
    }
 
@route("/api/albums/<album_id>/images/<fname>")
def image(album_id, fname):
    album = lib[album_id]
    return album[fname].detail()
 
@route("/thumbs/<album_id>/<fname>")
def thumb(album_id, fname):
    album = lib[album_id]
    image = album[fname]
    return bottle.static_file(image.thumb_basename, root=album.thumb_path)

if __name__ == "__main__":
    main()

