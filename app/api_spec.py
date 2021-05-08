"""OpenAPI v3 Specification"""

# apispec via OpenAPI
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin

# Create an APISpec
from app.schema.user_schema import UserCreate, User, UserLogin, AccessToken, RefreshToken

spec = APISpec(
    title="My App",
    version="1.0.0",
    openapi_version="3.0.2",
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)

# register schemas with spec
spec.components.schema("UserCreate", schema=UserCreate)
spec.components.schema("User", schema=User)
spec.components.schema("AccessToken", schema=AccessToken)
spec.components.schema("UserLogin", schema=UserLogin)
spec.components.schema("RefreshToken", schema=RefreshToken)
# add swagger tags that are used for endpoint annotation
tags = [
    {"name": "Authentication", "description": "For user authentication."},
]

for tag in tags:
    print(f"Adding tag: {tag['name']}")
    spec.tag(tag)
