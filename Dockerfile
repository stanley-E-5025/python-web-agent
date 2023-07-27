FROM python:3.11

WORKDIR /code
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/code

# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg

COPY requirements.txt requirements.txt
RUN python3 -m pip install -r requirements.txt

# Copy code
COPY api_v0/ code/
COPY web_drivers/ web_drivers/

EXPOSE 5000

CMD ["python3", "code/main.py"]
