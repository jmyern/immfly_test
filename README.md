# Solution

This solution was built using django as backend, and MySQL as de chosen database.

## Repositories

The content has been uploaded to a public github repository: https://github.com/jmyern/immfly_test.

The public Docker image for this repository is: ulisha/joan_immfly_interview

## Models

Models were created in the following way:
- Channel: Has many to many relations to other channels, content and groups to allow links to multiple sub_channels, content and groups. 
  - The use of signals (media_platform.signals) ensures that models cannot have both sub_channels and content at the same time as long as you are using the django interface and not editing the database directly. 
  - Could not get the same to work in the case that a channel has neither sub_channels nor content, because you cannot link many to many relations before save since id field still has not been assigned.
- Content: Has n to 1 relations with files and metadata.
  - Fields are stored in media folder.
  - Metadata is stored in the database as key and value to allow arbitrary metadata to be stored.
- Groups: Groups have many to many relations with channel to allow multiple channels to use the same group and for channels to use multiple groups.

All models are available to be edited on the django admin app.

## API

3 endpoints have been made available to get media channels and content:

- channel: Lists and filters channels that are not sub_channels to any other channel. Filters can be done through url parameters, the following are available:
  - ?id=&title=&language=&sub_channels=&content=&groups=
- channel/<channel_id>/subchannels: Lists and filters the sub_channels of a given channel. Filters can be done through url parameters, the following are available:
  - ?id=&title=&language=&sub_channels=&content=&groups=
- channel/<channel_id>/content: Lists and filters the content of a given channel. Filters can be done through url parameters, the following are available:
  - ?id=&rating=

The result of querying these endpoints will be a JSON with the corresponding information.

For relation fields, ids are returned, this could be changed to return the full string value if needed.

This was achieved by using the ListAPIView class of django rest framework along with serializers.

Groups has been made available as possible filter and will return a channel if any of it's sub_channels belongs to that group.

## Ratings

The management command to generate ratings is "calculate_ratings" and needs a path as parameter where it will store the .csv file with the ratings.

Ratings of all channels are in descending order, and channels without rating will not be listed.

## CI Actions

CI Actions have been created in .github/workflows. There are two different actions:
- django.yml: Will run the command "python manage.py test". This command will run all unit tests for this app. This action is triggered on push on the master branch.
- push.yml: Will build and push a new image on the Docker hub repository. This action is triggered on creation of a new release.

# Run

Can be run locally or through the docker image: ulisha/joan_immfly_interview.

Through Docker, it runs with gunicorn.

Static and Media files are cannot be recovered by default by simply running the container. To set this up, you need to set a proper production environment.

To set a production environment, you should follow these steps:
1. Create a shared folder with static and media content.
2. Run custom docker command to collect static data on the shared folder.
3. Create a proper reverse proxy (Apache, Nginx, etc...) with certificates and access to this shared folder to serve static and media content.
4. Set the reverse proxy to pass all petitions except /media/ and /static/ to this app.

## Parameters

Parameters are set through environment variables:
- IMMFLYTEST_DJANGO_KEY: Secret Key for Django
- IMMFLYTEST_DJANGO_DEBUG (optional): If value is "TRUE" will run on debug mode.
- IMMFLYTEST_DB_NAME: Name of MySQL database. Not needed if IMMFLYTEST_DJANGO_DEBUG is TRUE, since it will use a local sqlite file instead of MySQL.
- IMMFLYTEST_DB_USER: Username for MySQL. Not needed if IMMFLYTEST_DJANGO_DEBUG is TRUE, since it will use a local sqlite file instead of MySQL.
- IMMFLYTEST_DB_PASSWORD: Password for MySQL. Not needed if IMMFLYTEST_DJANGO_DEBUG is TRUE, since it will use a local sqlite file instead of MySQL.
- IMMFLYTEST_DB_HOST: Host of MySQL. Not needed if IMMFLYTEST_DJANGO_DEBUG is TRUE, since it will use a local sqlite file instead of MySQL.
- IMMFLYTEST_DB_PORT (optional): Port of MySQL, defaults to 3306. Not needed if IMMFLYTEST_DJANGO_DEBUG is TRUE, since it will use a local sqlite file instead of MySQL.

## Docker commands

Run Webservice through gunicorn:
```commandline
docker run --env-file env.list -p 80:8080 ulisha/joan_immflky_interview
```

Run tests
```commandline
docker run --env-file env.list -p 80:8080 ulisha/joan_immflky_interview python manage.py test
```

Run migrate
```commandline
docker run --env-file env.list -p 80:8080 ulisha/joan_immflky_interview python manage.py migrate
```

Run collect static
```commandline
docker run --env-file env.list -p 80:8080 ulisha/joan_immflky_interview python manage.py collectstatic
```