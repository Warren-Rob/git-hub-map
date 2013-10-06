import urllib, gzip, json, os
from celery.task import task
from heat_map.models import User, Location

@task(name='fetchData')
def fetch(url):
  fname = url.split('/')[-1]
  urllib.urlretrieve(url, fname)
  content = gzip.open(fname).read()
  d = json.loads(content)
  print d
  print a[1]

  return
  # download the file from gh archive

  # sift through the information and extract the relevant data
    # will be able to compile a list of usernames from the archive
    # iterate over each list, get location
    # with location, query google maps and get lng/lat
    # attempting to do so in the index will take tons more time!!

url = 'http://data.githubarchive.org/2012-04-11-15.json.gz'
fetch(url)
