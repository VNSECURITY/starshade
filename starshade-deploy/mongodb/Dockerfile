FROM mongo:latest
RUN mongo starshade-waf --eval "db.createCollection('waf');"

EXPOSE 27017
EXPOSE 28017
