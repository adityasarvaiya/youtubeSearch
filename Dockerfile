################# Builder ###############
FROM python:3.7-alpine AS base

RUN apk update && apk add --no-cache gcc libffi-dev g++ python3-dev build-base linux-headers postgresql-dev postgresql-contrib pcre-dev bash alpine-sdk \
  && pip install --upgrade pip && pip install wheel

COPY ./reqs/ ./reqs/
COPY requirements.txt .

RUN pip install -r requirements.txt

################# Release ###############
FROM python:3.7-alpine AS release

RUN apk add --update --no-cache bash libpq libjpeg-turbo libstdc++ postgresql-dev postgresql-contrib

COPY --from=base /usr/local/lib/python3.7/site-packages/ /usr/local/lib/python3.7/site-packages/
COPY --from=base /usr/local/bin/ /usr/local/bin/

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

ENV PATH=/root/local/bin:$PATH

WORKDIR /src

COPY . /src/

RUN mv /src/deploy/wait-for /bin/wait-for

#Copy over all the executable script
COPY ./deploy/entrypoint.sh /

#Grant executable permission to the startup script
RUN chmod +x /entrypoint.sh
RUN chmod +x /bin/wait-for

#Run Startup script
ENTRYPOINT ["/entrypoint.sh"]
