import requests
import jsonschema


def _headers(config):
    return {
        'X-DC-DEVKEY': config['api key'],
        'Accept': 'application/json'
    }

ME_RESPONSE_SCHEMA = {
    '$schema': 'http://json-schema.org/draft-07/schema#',

    "definitions": {
        'container': {
            'type': 'object',
            'properties': {
                'id': {'type': 'integer'},
                'public_id': {'type': 'string'},
                'name': {'type': 'string'},
                'parent_id': {'type': 'integer'},
                'template_id': {'type': 'integer'},
                'ekey': {'type': 'string'},
                'has_logo': {'type': 'boolean'},
                'is_active': {'type': 'boolean'},

                # additional property not in the spec,
                # but present in test responses
                'description': {'type': 'string'}
            },
            # 'required': [...],
            'additionalProperties': False
        },
        'access_role': {
            'type': 'object',
            'properties': {
                'id': {'type': 'integer'},
                'name': {'type': 'string'}
            },
            'required': ['id', 'name'],
            'additionalProperties': False
        }
    },

    'type': 'object',
    'properties': {
        'id': {'type': 'integer'},
        'username': {'type': 'string'},
        'account_id': {'type': 'integer'},
        'first_name': {'type': 'string'},
        'last_name': {'type': 'string'},
        'email': {'type': 'string'},
        'job_title': {'type': 'string'},
        'telephone': {'type': 'string'},
        'status': {'type': 'string'},
        'container': {'$ref': '#/definitions/container'},
        'access_roles': {
            'type': 'array',
            'items': {'$ref': '#/definitions/access_role'}
        },
        'is_cert_central': {'type': 'boolean'},
        'is_enterprise': {'type': 'boolean'},
        'has_container_assignments': {'type': 'boolean'},
        'container_visibility': {
            'type': 'array',
            'items': {'$ref': '#/definitions/container'}
        },

        # additional properties not in the spec,
        # but present in test responses
        'is_saml_sso_only': {'type': 'boolean'},
        'last_login_date': {'type': 'string'},
        'type': {'type': 'string'}
    },
    # 'required': [...],
    'additionalProperties': False
}

DOMAIN_LIST_RESPONSE_SCHEMA = {
    '$schema': 'http://json-schema.org/draft-07/schema#',

    "definitions": {
        'organization': {
            'type': 'object',
            'properties': {
                'id': {'type': 'integer'},
                'name': {'type': 'string'},
                'assumed_name': {'type': 'string'},
                'display_name': {'type': 'string'},

                # additional properties not in the spec,
                # but present in test responses
                'status': {'type': 'string'},
                'is_active': {} # {'type': 'boolean'}

            },
            # 'required': [...],
            'additionalProperties': False
        },
        'validation': {
            'type': 'object',
            'properties': {
                'date_created': {'type': 'string'},
                'type': {'type': 'string'},
                'name': {'type': 'string'},
                'description': {'type': 'string'},
                'status': {'type': 'string'},

                # additional property not in the spec,
                # but present in test responses
                'validated_until': {'type': 'string'}
            },
            'required': ['type', 'name', 'description', 'status'],
            'additionalProperties': False
        },
        'domain': {
            'type': 'object',
            'properties': {
                'id': {'type': 'integer'},
                'name': {'type': 'string'},
                'date_created': {'type': 'string'},
                'organization': {'$ref': '#/definitions/organization'},
                'validations': {
                    'type': 'array',
                    'items': {'$ref': '#/definitions/validation'}
                },
                'container': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'name': {'type': 'string'}
                    }
                },

                # additional properties not in the spec,
                # but present in test responses
                'dcv_method': {'type': 'string'},
                'is_active': {'type': 'boolean'}
            },
            # 'required': [...],
            'additionalProperties': False
        }
    },

    'type': 'object',
    'properties': {
        'domains': {
            'type': 'array',
            'items': {'$ref': '#/definitions/domain'}
        },

        # additional property not in the spec,
        # but present in test responses
        'page': {'type': 'object'}
    },
    # 'required': [...],
    'additionalProperties': False

}


def _make_request(config, api_path, schema, params=None):
    r = requests.get(
        config['endpoint uri'] + api_path,
        headers = _headers(config),
        params=params)
    r.raise_for_status()
    data = r.json()
    jsonschema.validate(data, schema)
    return data


def me(config):
    return _make_request(config, 'user/me', ME_RESPONSE_SCHEMA)


def list_domains(config, container_id):
    return _make_request(
        config=config,
        api_path='domain',
        schema=DOMAIN_LIST_RESPONSE_SCHEMA,
        params={'container_id': container_id})
