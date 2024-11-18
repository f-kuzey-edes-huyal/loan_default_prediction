FROM python:3.11-slim

WORKDIR /app

COPY ./requirements2.txt /app/




RUN apt-get update -y && apt-get install -y gcc  python3-dev

RUN pip install --no-cache-dir --upgrade -r /app/requirements2.txt

COPY ./modelxgb_i=93.bin  /app/

COPY ./main.py /app/

EXPOSE 8000
ENTRYPOINT  uvicorn main:app --host=0.0.0.0 --port=8000

#COPY main.py .

#COPY requirements2.txt .

#COPY ["main.py", "./"]
#COPY ["requirements2.txt", "./"]



#RUN pip install --upgrade pip 

# https://github.com/dask/dask-kubernetes/issues/238

#RUN apt-get update -y && apt-get install -y gcc  python3-dev

#RUN pip install -r requirements2.txt --default-timeout=1000 --no-cache-dir
#RUN pip install --default-timeout=100 -i https://pypi.org/simple -r requirements2.txt --no-cache-dir



#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]