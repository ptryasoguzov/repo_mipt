FROM python:3.6-slim-stretch
MAINTAINER Pavel Tryasoguzov <tryasoguzov.pe@phystech.edu>
COPY . .
RUN pip3 install -r requirements.txt
RUN rm -f app.db
RUN python3 ./db_create.py
EXPOSE 5000
CMD ["python", "app.py"]
