FROM ruby:2.5.3

RUN apt-get update -qq
RUN apt-get install build-essential default-mysql-client default-libmysqlclient-dev -y

RUN mkdir /opt/BHT-EMR-API
WORKDIR /opt/BHT-EMR-API
COPY tmp/BHT-EMR-API/Gemfile /opt/BHT-EMR-API/Gemfile
COPY tmp/BHT-EMR-API/Gemfile.lock /opt/BHT-EMR-API/Gemfile.lock
RUN bundle install
COPY tmp/BHT-EMR-API /opt/BHT-EMR-API

RUN mkdir /opt/eMastercard2Nart
WORKDIR /opt/eMastercard2Nart
COPY tmp/eMastercard2Nart/Gemfile /opt/eMastercard2Nart/Gemfile
COPY tmp/eMastercard2Nart/Gemfile.lock /opt/eMastercard2Nart/Gemfile.lock
RUN bundle install
COPY tmp/eMastercard2Nart /opt/eMastercard2Nart

COPY api/migration.sh /usr/bin/migration.sh
RUN chmod +x /usr/bin/migration.sh

COPY api/initialize_database.sh /usr/bin/initialize_database.sh
RUN chmod +x /usr/bin/initialize_database.sh

COPY api/backup_database.sh /usr/bin/backup_database.sh
RUN chmod +x /usr/bin/backup_database.sh
COPY api/restore_database.sh /usr/bin/restore_database.sh
RUN chmod +x /usr/bin/restore_database.sh

COPY api/correct_missing_dispensations.sh /usr/bin/correct_missing_dispensations.sh
RUN chmod +x /usr/bin/correct_missing_dispensations.sh

COPY api/change_database_password.sh /usr/bin/change_database_password.sh
RUN chmod +x /usr/bin/change_database_password.sh

COPY api/entrypoint.sh /usr/bin
RUN chmod +x /usr/bin/entrypoint.sh

ENTRYPOINT [ "entrypoint.sh" ]
EXPOSE 3000

CMD ["rails", "s", "-b", "0.0.0.0"]
