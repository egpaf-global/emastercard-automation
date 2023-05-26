#!/bin/bash

echo "Enter old database password: "
read -p '> ' -s OLD_PASSWORD

echo "Enter new database password: "
read -p '> ' -s NEW_PASSWORD

echo "Enter new database password again: "
read -p '> ' -s RE_NEW_PASSWORD

if [ $NEW_PASSWORD != $RE_NEW_PASSWORD ]; then
    echo "Passwords do not match"
    exit 255
fi

echo "use mysql; SET PASSWORD FOR 'root'@'%' = PASSWORD('$NEW_PASSWORD');" | mysql --host=mysqldb -u root --password=$OLD_PASSWORD || {
    echo "Password update failed!"
    exit 255
}
