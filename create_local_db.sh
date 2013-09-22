#!/bin/sh
#echo "Moving old test DB to test.sqlite.bak"
#mv $PYTHONPATH"/../db/test.sqlite" $PYTHONPATH"/../db/test.sqlite.bak"

echo "Creating new DB"
django-admin.py reset_db --router=default --noinput

django-admin.py syncdb --noinput

loaddata() {
	echo "Importing "$2
	django-admin.py loaddata $PYTHONPATH/app/fixtures/$2
}

###############################################################################
# Load data
###############################################################################
loaddata app "auth.json"


