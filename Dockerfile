FROM python:latest

EXPOSE 3000

WORKDIR /home/app

COPY requirements.txt /home/app

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY ./todo.txt /todo.txt
COPY ./app/templates/* /home/app/templates/
COPY ./app/static/* /home/app/static/
COPY ./app/app.py /home/app/

CMD [ "python3", "-m" , "flask", "run", "--host=127.0.0.1", "--port=3000"]
