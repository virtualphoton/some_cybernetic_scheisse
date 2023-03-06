FROM python:3-alpine3.17
WORKDIR /workapp
COPY . /workapp
RUN pip install -r requirements.txt
EXPOSE 5000
CMD flask --app ./app.py run -h 0.0.0.0 -p 5000