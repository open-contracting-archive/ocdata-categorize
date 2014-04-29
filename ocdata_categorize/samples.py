import csv
import os
import requests


def get_resource_path(name, url, cache=True):
    """
    Returns a path to a cached file based on a name and a url.
    If cache=False or file is not available, then goes and gets the
    file and adds it to the cache and then returns the path.
    """
    path = '.cache/%s.csv' % name
    if cache and os.path.exists(path):
        return path
    else:
        response = requests.get(url)
        assert response.status_code == 200, 'Cannot access resource'
        if not os.path.exists('.cache'):
            os.mkdir('.cache')
        with open(path, 'w') as o:
            o.write(response.content)
        return path


def get_data(name, url=None, path=None, cache=True):
    if url:
        path = get_resource_path(name, url, cache=cache)
    with open(path) as o:
        rows = csv.reader(o.read().split('\n'))
    header = None
    data = []
    for row in rows:
        if header:
            data.append(dict(zip(header, row)))
        else:
            header = row
    return data


def set_of_values(s, original_key):
    result = set()
    for s in original_key.split(','):
        s = s.strip()
        if s:
            result.add()


def get_entities(line, entity_key):
    entities = line[entity_key] or '?'
    entities = set([x.strip() for x in entities.split(',') if x.strip()])
    return entities


def load_samples(data, original_key, entity_key, url=False, cache=True):
    samples = []
    for name, resource in data.iteritems():
        if url:
            data = get_data(name, url=resource, path=None, cache=cache)
        else:
            data = get_data(name, url=None, path=resource, cache=cache)
        last_name = None  # what is this for?
        for line in data:
            header = line[original_key] or last_name
            last_name = header
            for entity in get_entities(line, entity_key):
                samples.append(
                    {'header': header,
                     'entity': entity,
                     'sample': name}
                )
    return samples
