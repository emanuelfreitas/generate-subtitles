FROM python:slim

LABEL maintainer="Emanuel Freitas <emanuelfreitas@outlook.com>"

RUN echo "deb http://deb.debian.org/debian buster main contrib non-free" > /etc/apt/sources.list && \
    echo "deb http://deb.debian.org/debian buster-updates main contrib non-free" >> /etc/apt/sources.list && \
    echo "deb http://deb.debian.org/debian buster-backports main contrib non-free" >> /etc/apt/sources.list && \
    apt-get update && apt-get install -qq -y ffmpeg && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir openai-whisper googletrans

COPY src /app

ENTRYPOINT ["python", "-u", "/app/generate-subtitles.py"]