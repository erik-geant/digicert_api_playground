import json
import logging

import click
import jsonschema

from dctests import dcapi

logger = logging.getLogger(__name__)

CONFIG_SCHEMA = {
    '$schema': 'http://json-schema.org/draft-07/schema#',

    'type': 'object',
    'properties': {
        'endpoint uri': {'type': 'string'},
        'api key': {'type': 'string'}
    },
    'required': ['endpoint uri', 'api key'],
    'additionalProperties': False
}


def validate_config(ctx, param, f):
    """
    loads, validates and returns configuration parameters

    :param ctx:
    :param param:
    :param f: open file object
    :return: a dict containing configuration parameters
    """
    try:
        config = json.loads(f.read())
        jsonschema.validate(config, CONFIG_SCHEMA)
    except (json.JSONDecodeError, jsonschema.ValidationError) as e:
        raise click.BadParameter(str(e))

    dcapi.me(config)

    return config


@click.command()
@click.option(
    '--config',
    required=True,
    type=click.File('r'),
    callback=validate_config,
    help='configuration filename')
def cli(config):

    me = dcapi.me(config)

    def _domains():
        for c in me['container_visibility']:
            domains = dcapi.list_domains(config, c['id'])
            for d in domains['domains']:
                yield d

    for d in _domains():
        logger.info(d['name'])
        if not d.get('is_active', False):
            logger.info('\tinactive')
            continue

        for v in d.get('validations', []):
            logger.info('\ttype: %s [%s]' % (v['name'], v['status']))
            if 'date_created' in v:
                logger.info('\t\tcreated: %s' % v['date_created'])
            if 'validated_until' in v:
                logger.info('\t\tuntil: %s' % v['validated_until'])


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    cli()

