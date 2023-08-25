FROM python:3.10.9

WORKDIR mast-app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD [ "python", "app.py"]
