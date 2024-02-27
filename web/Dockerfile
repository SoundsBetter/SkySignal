FROM python
LABEL authors="SoundsBetter"

WORKDIR /usr/src/web

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/web/entrypoint.sh
RUN chmod +x /usr/src/web/entrypoint.sh

COPY . .

ENTRYPOINT ["/usr/src/web/entrypoint.sh"]