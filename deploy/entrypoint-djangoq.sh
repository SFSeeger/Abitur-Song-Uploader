#!/bin/bash

/app/web/manage.py migrate
/app/web/manage.py createcachetable

/app/web/manage.py qcluster
