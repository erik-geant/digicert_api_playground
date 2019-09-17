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


def _make_request(config, api_path, schema):
    r = requests.get(
        config['endpoint uri'] + 'user/me',
        headers = _headers(config))
    r.raise_for_status()
    data = r.json()
    jsonschema.validate(data, schema)


def me(config):
    return _make_request(config, 'user/me', ME_RESPONSE_SCHEMA)
