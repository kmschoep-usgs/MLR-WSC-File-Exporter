import os

PROJECT_DIR = PROJECT_DIR = os.path.dirname(__file__)
DEBUG = False

# These configuration parameters configure where the file that is created is written to.
S3_BUCKET = os.getenv('S3_BUCKET', 'mlr-exports') + '-' + os.getenv('TIERNAME', 'development')
AWS_REGION = os.getenv('AWS_REGION', 'us-west-2')
S3_ENDPOINT_URL = os.getenv('S3_ENDPOINT_URL', None)

# The following six variables configure authentication

# If using a JWK Set, set the environment variable AUTH_JWKS_URL to the url where it can be retrieved
AUTH_JWKS_URL = os.getenv('oauth_server_jwks_url')

# If using a public key, set the environment variable AUTH_TOKEN_KEY_URL to the url where it can be retrieved
AUTH_TOKEN_KEY_URL = os.getenv('oauth_server_token_key_url')

# Set the path to the certificate for AUTH_JWKS_URL/AUTH_TOKEN_KEY_URL. If set to False then, SSL verification will not occur.
AUTH_CERT_PATH = os.getenv('oauth_server_cert_path', True)

# If using the above, use the AUTH_TOKEN_KEY_ALGORITHM to set the algorithm. By default it will be RS256
JWT_ALGORITHM = os.getenv('jwt_algorithm', 'HS256')

# Set the JWT_DECODE_AUDIENCE environment variable to the value of the 'aud' claim in the
JWT_DECODE_AUDIENCE = os.getenv('jwt_decode_audience')

# Define the function that retrieves the roles from the JWT and assign to JWT_ROLE_CLAIM.
def get_roles(dict):
    return dict.get('authorities')
JWT_ROLE_CLAIM = get_roles

# Set the allowed_roles
AUTHORIZED_ROLES = [role.strip() for role in os.getenv('authorized_roles', '').split(',')]

# Configure exception JSON to not always output with a `message` field. Global exception handling is done via a custom handler in services.py.
ERROR_INCLUDE_MESSAGE=False