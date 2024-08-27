FROM python:3.9.12
RUN mkdir /app
WORKDIR /app/
ADD . /app/
RUN pip install Flask
CMD ["python","/app/app.py"]