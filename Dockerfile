FROM ruby:2.7.0

RUN apt-get update
RUN apt-get install build-essential default-mysql-client default-libmysqlclient-dev pv -y

RUN mkdir /opt/emr-DRC
WORKDIR /opt/emr-DRC
COPY tmp/emr-DRC/Gemfile /opt/emr-DRC/Gemfile
COPY tmp/emr-DRC/vendor /opt/emr-DRC/vendor
RUN bundle install --local
COPY tmp/emr-DRC /opt/emr-DRC
COPY api/puma.rb /opt/emr-DRC/config/puma.rb

COPY api/bin/migration.sh /usr/bin/migration.sh
RUN chmod +x /usr/bin/migration.sh

COPY api/bin/initialize_database.sh /usr/bin/initialize_database.sh
RUN chmod +x /usr/bin/initialize_database.sh

COPY api/bin/update_metadata.sh /usr/bin/update_metadata.sh
RUN chmod +x /usr/bin/update_metadata.sh

COPY api/bin/backup_database.sh /usr/bin/backup_database.sh
RUN chmod +x /usr/bin/backup_database.sh

COPY api/bin/restore_database.sh /usr/bin/restore_database.sh
RUN chmod +x /usr/bin/restore_database.sh

COPY api/bin/correct_missing_dispensations.sh /usr/bin/correct_missing_dispensations.sh
RUN chmod +x /usr/bin/correct_missing_dispensations.sh

COPY api/bin/fix_loose_dispensations.sh /usr/bin/fix_loose_dispensations.sh
RUN chmod +x /usr/bin/fix_loose_dispensations.sh

COPY api/bin/change_database_password.sh /usr/bin/change_database_password.sh
RUN chmod +x /usr/bin/change_database_password.sh

COPY api/bin/fix_vl_ldl_results.sh /usr/bin/fix_vl_ldl_results.sh
RUN chmod +x /usr/bin/fix_vl_ldl_results.sh

COPY api/bin/entrypoint.sh /usr/bin
RUN chmod +x /usr/bin/entrypoint.sh


COPY api/bin/fix_duplicate_ipts.sh /usr/bin
RUN chmod +x /usr/bin/fix_duplicate_ipts.sh

COPY api/bin/fix_viral_load_results.sh /usr/bin/fix_viral_load_results.sh
RUN chmod +x /usr/bin/fix_viral_load_results.sh


ENTRYPOINT [ "entrypoint.sh" ]
EXPOSE 3000

CMD ["rails", "s", "-b", "0.0.0.0"]
