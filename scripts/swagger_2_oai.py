import json, requests, os, collections

_prefix = '<html><body><pre>'
CONVERTER = "https://mermade.org.uk/api/v1/convert"

dir_path = os.path.dirname(os.path.realpath(__file__))

config1 = {
    'TARGET': 'file',
    'BEFORE_OAI': dir_path + '/resource.json',
    'AFTER_OAI': dir_path + '/oai.json',
    'SOURCE_SWAGGER_API': 'http://127.0.0.1:5000/api/v2/'

}
config = {
    'TARGET': 'api',
    'BEFORE_OAI': 'http://10.0.2.2:8081/openapi.json',
    'AFTER_OAI': 'http://10.0.2.2:8081/swagger-editor/backend_openapi.yaml',
    'SOURCE_SWAGGER_API': 'http://127.0.0.1:5000/api/v2/'
}


def log(message, type='info'):
    print(message)


def attach_dict(dest, source):
    """
    copy source structure data to dest and store
    :param dest: destination object dict|list
    :param source: source object dict|list
    :return: None
    """
    if isinstance(dest, dict):
        if isinstance(source, dict):
            for item, value in source.items():
                if item in dest:
                    if isinstance(dest[item], dict) or isinstance(dest[item], list):
                        attach_dict(dest[item], value)
                    else:
                        dest[item] = value
                else:
                    dest[item] = value
    elif isinstance(dest, list):
        if isinstance(source, list):
            dest += source
        else:
            dest.append(source)


def array_merge(dest, source):
    """
    Merge array from source to dest and store in dest. Apply for xtag-Groups and tags
    :param list dest:
    :param list source:
    :return: None
    """

    for item_source in source:
        # check if item with name in source
        if isinstance(item_source, dict) and item_source.get('name'):
            flag = True
            for item_dest in dest:
                if isinstance(item_dest, dict) and item_dest.get('name') and item_source.get('name') == item_dest.get(
                        'name'):
                    flag = False
                    if item_dest.get('tags') and isinstance(item_dest['tags'], list):
                        array_merge(item_dest['tags'], item_source['tags'])
                    break
            if flag:
                dest.append(item_source)


        else:
            flag = True
            for ite in dest:
                if ite == item_source:
                    flag = False
                    break
            if flag:
                dest.append(item_source)


def dict_merge(dct, merge_dct, overwrite_des=True):
    """ Recursive dict merge. Inspired by :meth:``dict.update()``, instead of
    updating only top-level keys, dict_merge recurses down into dicts nested
    to an arbitrary depth, updating keys. The ``merge_dct`` is merged into
    ``dct``.
    :param dct: dict onto which the merge is executed
    :param merge_dct: dct merged into dct
    :return: None
    """
    for k, v in merge_dct.items():
        if (k in dct and isinstance(dct[k], dict)
                and isinstance(merge_dct[k], collections.Mapping)):
            dict_merge(dct[k], merge_dct[k])
        else:
            dct[k] = merge_dct[k]


def merge_oai(dest, source):
    # merge paths:
    dict_merge(dest['paths'], source['paths'])
    dict_merge(dest['components'], source['components'])
    # merge tags
    array_merge(dest['tags'], source['tags'])
    array_merge(dest['x-tagGroups'], source['x-tagGroups'])


def orderOAI(source_json):
    ord_dict = collections.OrderedDict()
    for key in ['openapi', 'info', 'tags', 'servers', 'x-tagGroups', 'paths', 'components']:
        ord_dict[key] = source_json[key]
    return ord_dict


def get_resource(config):
    if config['TARGET'] == 'file':
        log("Source Open API json file exists, reading....")
        f = open(config['BEFORE_OAI'], "r")
        source_json = json.loads(f.read())
        f.close()
        return source_json


    elif config['TARGET'] == 'api':
        log("Reading source Open API data json from ({})".format(config['BEFORE_OAI']))
        rv = requests.get(config['BEFORE_OAI'])
        if rv.status_code == 200:
            return json.loads(rv.text)
        else:
            log('Cannot get data from BEFORE OAI')
            exit(code=1)
    else:
        return {}


def write_source(des_json, config):
    log("Writing result.....")
    if config['TARGET'] == 'file':
        f_out = config['AFTER_OAI']
        log("Writing result to file ({})....".format(f_out))
        f = open(f_out, 'w')
        f.write(json.dumps(des_json))
        f.close()
    elif config['TARGET'] == 'api':
        log('Posting result to API docs ({})....'.format(config['AFTER_OAI']))
        headers = {
            'content-Type': 'application/yaml'
        }
        rv = requests.put(config['AFTER_OAI'], data=json.dumps(des_json), headers=headers, )
        log("Result code: {} .{}".format(rv.status_code, rv.text if rv.status_code == 200 else ''))
    log("Finished successfully.")


if __name__ == '__main__':

    # Get swagger json, ignore catching exception
    url = config['SOURCE_SWAGGER_API'] + 'swagger.json'
    log("Geting swagger json data (url={}).....".format(url))
    rv = requests.get(url=url)

    requests_header = {
        'accept': 'application/json'
    }
    data = {
        'source': rv.text
    }

    log("Sending to ({})....".format(CONVERTER))
    rv = requests.post(url=CONVERTER, data=data, headers=requests_header)
    if rv.status_code == 200:
        response = rv.text.replace(_prefix, '')
        log("Successfully converted swagger data to OAI 3.0.....")
        source_json = get_resource(config)

        des_json = json.loads(response)
        log("Merging destination OAI to source OAI..............")
        merge_oai(source_json, des_json)
        write_source(source_json, config)
