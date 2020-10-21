FROM python:3.8
COPY . /app
RUN pip install -r /app/requirements.txt
EXPOSE 5000
CMD python3 /app/index.py
