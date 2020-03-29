FROM ruby:2.5.3

RUN apt-get update -qq
RUN apt-get install build-essential default-mysql-client default-libmysqlclient-dev -y

RUN mkdir /opt/BHT-EMR-API
WORKDIR /opt/BHT-EMR-API
COPY BHT-EMR-API/Gemfile /opt/BHT-EMR-API/Gemfile
RUN bundle install
COPY BHT-EMR-API /opt/BHT-EMR-API
COPY api-config.yml /opt/BHT-EMR-API/config/database.yml

RUN mkdir /opt/eMastercard2Nart
WORKDIR /opt/eMastercard2Nart
COPY eMastercard2Nart/Gemfile /opt/eMastercard2Nart/Gemfile
COPY eMastercard2Nart/Gemfile.lock /opt/eMastercard2Nart/Gemfile.lock
RUN bundle install
COPY eMastercard2Nart /opt/eMastercard2Nart
COPY migration-config.yml /opt/eMastercard2Nart/config.yaml

COPY migration.sh /usr/bin/migration.sh
RUN chmod +x /usr/bin/migration.sh
COPY initialize_database.sh /usr/bin/initialize_database.sh
RUN chmod +x /usr/bin/initialize_database.sh
COPY entrypoint.sh /usr/bin
RUN chmod +x /usr/bin/entrypoint.sh
ENTRYPOINT [ "entrypoint.sh" ]
EXPOSE 8000

CMD ["rails" "s", "-b", "0.0.0.0", "-p", "8000"]
