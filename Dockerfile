FROM python:3.11

WORKDIR /code
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/code

# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg

RUN apt-get update && apt-get install -y wget gnupg \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update && apt-get install -y google-chrome-stable


COPY requirements.txt requirements.txt
RUN python3 -m pip install -r requirements.txt



# Copy code
COPY api_v0/ code/



EXPOSE 5000

CMD ["python3", "code/main.py"]
