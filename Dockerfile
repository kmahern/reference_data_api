FROM python:3.11

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./reference_data_app /code/reference_data_app

EXPOSE 8000

CMD ["uvicorn", "--reload", "reference_data_app.main:app", "--host", "0.0.0.0", "--port", "8000"]