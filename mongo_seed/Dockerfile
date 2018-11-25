FROM mongo:4.0.4-xenial

COPY data/restaurant.json /init.json
CMD mongoimport --host mongodb --db restaurants_db --collection restaurant --type json --file /init.json
