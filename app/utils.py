import json
from keycloak import KeycloakAdmin, KeycloakOpenID
from flask import current_app


def get_keycloak_admin():
    """Get Keycloak Admin instance configured with app settings."""
    return KeycloakAdmin(
        server_url=current_app.config.get("SERVER_URL"),
        username=current_app.config.get("ADMIN_USERNAME"),
        password=current_app.config.get("ADMIN_PASS"),
        realm_name=current_app.config.get("REALM_NAME"),
        verify=True,
    )


def get_keycloak_oid_client():
    """Get Keycloak OpenID Connect client instance configured with app settings."""
    return KeycloakOpenID(
        server_url=current_app.config.get("SERVER_URL"),
        client_id=current_app.config.get("CLIENT_ID"),
        realm_name=current_app.config.get("REALM_NAME"),
        client_secret_key=current_app.config.get("CLIENT_SECRET"),
        verify=True,
    )


def client_exists():
    """Check if the Keycloak OpenId Connect client exists."""
    admin = get_keycloak_admin()
    client = admin.get_client_id(client_id=current_app.config.get("CLIENT_ID"))

    return client is not None


def create_client():
    """Create the required Keycloak OpenId Connect client."""
    admin = get_keycloak_admin()
    client_config = json.load(open("app/config/oid_client_config.json"))

    try:
        client = admin.create_client(client_config)
    except Exception as e:
        print(f"Error creating client: {e}")
        return None

    return client


def ensure_client_exists():
    """Ensure the Keycloak client exists, create it if not."""
    if not client_exists():
        return create_client()
    return True
