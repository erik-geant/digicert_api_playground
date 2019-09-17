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

    logger.warning(dcapi.me(config))

    return config

@click.command()
@click.option(
    '--config',
    required=True,
    type=click.File('r'),
    callback=validate_config,
    help='configuration filename')
def cli(config):

    print(config)

if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG)
    cli()

