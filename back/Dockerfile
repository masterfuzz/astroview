FROM archlinux

RUN pacman -Sy && \
    pacman --noconfirm -S python python-pip imagemagick perl-image-exiftool libraw

WORKDIR /app

COPY requirements.txt ./

RUN python -m pip install -r requirements.txt

COPY src/ .
COPY docker-config.yaml ./config.yaml


CMD [ "python", "web.py" ]