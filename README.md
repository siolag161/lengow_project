Lengow Project
============

A heavily personalized project template for Django 1.8.4 using Postgres for development and production.
Ready to deploy on Heroku with a bunch of other goodies.

Forked from the original [django-kevin](https://github.com/imkevinxu/django-kevin)

Running Your Project
=====================

For development:

    workon lengow-dev
    sudo pip install --upgrade pip
    sudo pip install --upgrade setuptools
    sudo env ARCHFLAGS="-arch i386 -arch x86_64" pip install psycopg2
    sudo pip install -r requirements/dev.txt

For testing:

    workon lengow-test
    sudo pip install --upgrade pip
    sudo pip install --upgrade setuptools
    sudo env ARCHFLAGS="-arch i386 -arch x86_64" pip install psycopg2
    sudo pip install -r requirements/test.txt

For switching between 2 modes: we use 2 scripts

    ./dev_mode.sh
    ./test_mode.sh

Install node packages
---------------------

*Prerequisites: node*

    sudo npm install

Sometimes the install may stall or not install everything. Try running `npm list` and then manually installing anything that may be missing.

One-time system installs
------------------------

*Prerequisites: homebrew*

In order to use the grunt task runner you need to install it globally:

    sudo npm install -g grunt-cli

In order to be able to lint SCSS files locally you need `ruby` on your local system and a certain gem. See [https://github.com/ahmednuaman/grunt-scss-lint#scss-lint-task](https://github.com/ahmednuaman/grunt-scss-lint#scss-lint-task)

    gem install scss-lint

In order to use django-pipeline for post-processing, you need `yuglify` installed on your local system:

    sudo npm install -g yuglify

In order for grunt to notify you of warnings and when the build is finished, you need a [notification system](https://github.com/dylang/grunt-notify#notification-systems) installed. Below is the Mac OSX notification command-line tool:

    brew install terminal-notifier

In order to use Redis for caching and queuing, you need to download it and have it running in the background.
This will also set `redis-server` to automatically run at launch:

    brew install redis (for Mac)
    ln -sfv /usr/local/opt/redis/*.plist ~/Library/LaunchAgents
    launchctl load ~/Library/LaunchAgents/homebrew.mxcl.redis.plist
    launchctl start ~/Library/LaunchAgents/homebrew.mxcl.redis.plist

Development Mode
================

Set .env.dev variable for dev
-----------------------------

The environment variables for development sets the appropriate `DJANGO_SETTINGS_MODULE` and `PYTHONPATH` in order to use `django-admin.py` seemlessly. Necessary for Foreman and other worker processes

*`.env.dev` is not version controlled so the first person to create this project needs to create a `.env.dev` file for Foreman to read into the environment. Future collaboraters need to email the creator for it.*

    echo DJANGO_SETTINGS_MODULE=config.settings.dev >> .env.dev
    echo PYTHONPATH=lengow >> .env.dev
    echo PYTHONUNBUFFERED=True >> .env.dev
    echo PYTHONWARNINGS=ignore:RemovedInDjango19Warning >> .env.dev
    echo CACHE=dummy >> .env.dev

Recommended to use foreman to use development environment variables and processes:

    echo "env: .env.dev" > .foreman
    echo "procfile: Procfile.dev" >> .foreman

Compile initial static assets
-----------------------------

This will compile all the files in `/lengow/static` for the first run.

    grunt build

Create local postgres database for dev
--------------------------------------

*Prerequisites: Postgres and Heroku Toolbelt*

Install Postgres for your OS [here](http://www.postgresql.org/download/). For Max OSX the easiest option is to download and run [Postgres.app](http://postgresapp.com/).

    # Make sure Postgres.app is running
    workon lengow-dev
    createdb lengow-dev
    foreman run django-admin.py migrate

Run project locally in dev environment
--------------------------------------

Use the right virtual environment:

    workon lengow-dev

Start the server with:

    foreman start

Create a local super user with:

    foreman run django-admin.py createsuperuser

To run one-off commands use:

    foreman run django-admin.py COMMAND

To enable Live Reload, download and turn on a [browser extension](http://feedback.livereload.com/knowledgebase/articles/86242-how-do-i-install-and-use-the-browser-extensions-).

Production Mode
===============

Set .env variable for prod
--------------------------

The environment variables for production must contain a separate `SECRET_KEY` for security and the appropriate `DJANGO_SETTINGS_MODULE` and `PYTHONPATH` in order to use `django-admin.py` seemlessly. Hacky use of `date | md5` to generate a pseudo-random string.

*`.env` is not version controlled so the first person to create this project needs to create a `.env` file for Foreman and Heroku to read into the environment. Future collaboraters need to email the creator for it.*

    echo -n SECRET_KEY=`date | md5` >> .env (for MAC, for Linux we have md5sum which is quite similar)
    sleep 1
    echo `date | md5` >> .env
    echo DJANGO_SETTINGS_MODULE=config.settings.prod >> .env
    echo PYTHONPATH=lengow >> .env
    echo WEB_CONCURRENCY=3 >> .env
    echo PYTHONUNBUFFERED=True >> .env
    echo PYTHONWARNINGS=ignore:RemovedInDjango19Warning >> .env
    echo BUILDPACK_URL=https://github.com/heroku/heroku-buildpack-multi.git >> .env

Deploy to Heroku
----------------

*Prerequisites: Heroku Toolbelt and heroku-config*

First step is to deploy to Heroku with the `post_compile` script in `/bin` so that node functions can be installed for python to call them.

    git init
    git add .
    git commit -m "Ready for initial Heroku deploy"
    heroku create
    heroku config:push
    git push heroku master

After `post_compile` is successful, uncomment the line with the variable `STATICFILES_STORAGE` in `/lengow/config/settings/base.py` to enable django-pipeline and push again.

    git commit -am "Enabled django-pipeline"
    git push heroku master
    heroku run django-admin.py migrate
    heroku open

To run one-off commands like `createsuperuser` use:

    heroku run django-admin.py COMMAND

Debugging tip: sometimes purging the cache can help fix a random error. Just run:

    heroku run django-admin.py clear_cache

Run project locally in prod environment
---------------------------------------

Set the `.foreman` file to use production environment variables and processes:

    echo "env: .env" > .foreman
    echo "procfile: Procfile" >> .foreman

Use the right virtual environment:

    workon lengow-prod

This is meant to mimic production as close as possible using both the production database and environment settings so proceed with caution.

**WARNING**: If this project has SSL turned on, [localhost:5000](http://localhost:5000) won't work anymore because it will always try to redirect to [https://localhost:5000](https://localhost:5000). To fix this comment out the SECURITY CONFIGURATION section in `/lengow/config/settings/prod.py`

    heroku config:pull
    foreman run django-admin.py collectstatic --noinput
    foreman start

The site will be located at [localhost:5000](http://localhost:5000)

Testing Mode
============

Set .env.test variable for test
------------------------------

The environment variables for testing sets the appropriate `DJANGO_SETTINGS_MODULE` and `PYTHONPATH` in order to use `django-admin.py` seemlessly. Necessary for Foreman and other worker processes

*`.env.test` is not version controlled so the first person to create this project needs to create a `.env.test` file for Foreman to read into the environment. Future collaboraters need to email the creator for it.*

    echo DJANGO_SETTINGS_MODULE=config.settings.test >> .env.test
    echo PYTHONPATH=lengow >> .env.test
    echo PYTHONUNBUFFERED=True >> .env.test
    echo PYTHONWARNINGS=ignore:RemovedInDjango19Warning >> .env.test

Run tests locally in test environment
-------------------------------------

Set the `.foreman` file to use testing environment variables and processes:

    echo "env: .env.test" > .foreman
    echo "procfile: Procfile.test" >> .foreman

Use the right virtual environment:

    workon lengow-test

And have static assets prepared (for coverage tests):
    
    grunt build
    foreman run django-admin.py collectstatic --noinput

Automatically run all tests and linters and watch files to continuously run tests:

    foreman start

You can view the results of the tests in HTML at [localhost:9000/tests](http://localhost:9000/tests)

You can specifically view the results of Django coverage tests at [localhost:9000/tests/django](http://localhost:9000/tests/django)

Jasmine JS Unit Tests
---------------------

Grunt automatically compiles Jasmine tests written in CoffeeScript at `/lengow/static/js/tests/coffee` and runs the tests upon every save.

You can specifically view the results of Jasmine JS unit tests at [localhost:9000/tests/jasmine](http://localhost:9000/tests/jasmine)

You can specifically view the results of JS coverage tests at [localhost:9000/tests/jasmine/coverage.html](http://localhost:9000/tests/jasmine/coverage.html)

Add-ons & Services
==================

SSL
---
Enable SSL via Heroku, Cloudflare, or your DNS provider and then uncomment the SECURITY CONFIGURATION section in `/lengow/config/settings/prod.py` to enable security best practices for production.

Invoke
------
Scripts can be programmed to be run on the command-line using [Invoke](https://github.com/pyinvoke/invoke) for repeated tasks like deployment, building, or cleaning. Write your tasks in `tasks.py`.

Redis Cloud Caching
-------------------
In order to enable redis for caching and queues, add [Redis Cloud](https://devcenter.heroku.com/articles/rediscloud) to Heroku.

    heroku addons:add rediscloud:25

Redis Queue Worker
------------------
Add a [Redis Queue](https://github.com/ui/django-rq) worker process to Procfile:

    echo "worker: django-admin.py rqworker high default low" >> Procfile

Push the changed Procfile to Heroku:

    git add Procfile
    git commit -m "Added worker process to Procfile, pushing to Heroku"
    git push heroku master

Turn on background job worker with this one-liner:

    heroku scale worker=1

Redis Queue Scheduler
---------------------
Add a [RQ Scheduler](https://github.com/ui/rq-scheduler) process to Procfile:

    echo "scheduler: rqscheduler --url \$REDISCLOUD_URL" >> Procfile

Push the changed Procfile to Heroku:

    git add Procfile
    git commit -m "Added scheduler process to Procfile, pushing to Heroku"
    git push heroku master

Turn on background job scheduler with this one-liner:

    heroku scale scheduler=1

Amazon S3
---------
To use Amazon S3 as a static and media file storage, create a custom Group and User via IAM and then a custom static bucket and media bucket with public read policies.

Add the following config variables to Heroku:

    heroku config:set AWS_ACCESS_KEY_ID=INSERT_ACCESS_KEY_ID
    heroku config:set AWS_SECRET_ACCESS_KEY=INSERT_SECRET_ACCESS_KEY
    heroku config:set AWS_STATIC_STORAGE_BUCKET_NAME=lengow-static
    heroku config:set AWS_MEDIA_STORAGE_BUCKET_NAME=lengow-media

Monitoring
----------
- [Librato](https://devcenter.heroku.com/articles/librato) for Heroku performance monitoring
- [New Relic](https://devcenter.heroku.com/articles/newrelic) for server performance monitoring (protip: set [availability monitoring](https://coderwall.com/p/u0x3nw) on to avoid Heroku idling)
- [RedisMonitor](https://devcenter.heroku.com/articles/redismonitor) for Redis server monitoring
- [Logentries](https://devcenter.heroku.com/articles/logentries) provides logging backups as well as search and notifications. Can also additionally backup to S3
- [Sentry](https://devcenter.heroku.com/articles/sentry) for error tracking with [Raven](http://raven.readthedocs.org/en/latest/index.html) as the client. Make sure to use a [synchronous blocking transport](http://python-rq.org/patterns/sentry/).
- [Ranger](https://devcenter.heroku.com/articles/ranger) to alert you when your app is down

Testing
-------
- [Rainforest QA](https://devcenter.heroku.com/articles/rainforest) for simple integration testing
- [Tinfoil Security](https://devcenter.heroku.com/articles/tinfoilsecurity) for regularly scanning your app for security vulnerabilities
- [Loader.io](https://devcenter.heroku.com/articles/loaderio) for load testing

Continuous Integration
----------------------
Includes a fancy badge for GitHub README

- [Travis CI](https://travis-ci.org/) for continuous integration testing
- [Coveralls.io](https://coveralls.io/) for coverage testing
- [Requires.io](https://requires.io/) for dependency management

Utilities
---------
- [Filepicker](https://devcenter.heroku.com/articles/filepicker) for file uploading and content management
- [Twilio](http://www.twilio.com/) for sending SMS, MMS, and Voice. Recommended to use [`django-twilio`](http://django-twilio.readthedocs.org/en/latest/)
- [Mailgun](https://devcenter.heroku.com/articles/mailgun) or [Sendgrid](https://devcenter.heroku.com/articles/sendgrid) for email sending. Here are some useful [email templates](http://blog.mailgun.com/transactional-html-email-templates/)
- [MailChimp](http://mailchimp.com/) for email newsletters or create your own [custom newsletter emails](http://zurb.com/playground/responsive-email-templates)

