# !/bin/sh

# init & create migrations
python manage.py db init

# first migrate
python manage.py db migrate -m "init"

# upgrade database
python manage.py db upgrade

# create Roles
python manage.py shell

# adduser
python manage.py adduser neo1218 neo1218@yeah.net

# done!
echo "\n"
echo "------------------------------------"
echo "create test database done!"
echo "database: data-dev.sqlite"
echo "test user: neo1218 neo1218@yeah.net"
echo "------------------------------------"
