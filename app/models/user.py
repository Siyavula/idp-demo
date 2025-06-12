from app.utils import get_keycloak_admin, get_keycloak_oid_client


class KeycloakUser:
    """Class representing a user in Keycloak."""

    def __init__(self):
        self.admin = get_keycloak_admin()
        self.client = get_keycloak_oid_client()
        self.user_id = None
        self.username = None
        self.email = None
        self.first_name = None
        self.last_name = None
        self._password = None

    @classmethod
    def create_new(cls, username, password, email, first_name, last_name):
        """Factory method for creating a new user."""
        user = cls()
        user.username = username
        user._password = password
        user.email = email
        user.first_name = first_name
        user.last_name = last_name

        # Check if user already exists
        existing_id = user._get_user_id_by_username(username)
        if existing_id:
            raise ValueError(f"User {username} already exists")

        # Create the user
        user.user_id = user.admin.create_user(user._serialize_for_creation())

        return user

    @classmethod
    def from_username(cls, username):
        """Factory method for retrieving existing user by username."""
        user = cls()
        user.username = username
        user.user_id = user._get_user_id_by_username(username)

        if not user.user_id:
            raise ValueError(f"User {username} not found")

        user._load_user_details()

        return user

    @classmethod
    def from_user_id(cls, user_id):
        """Factory method for retrieving existing user by ID."""
        user = cls()
        user.user_id = user_id

        user._load_user_details()

        return user

    @classmethod
    def get_or_create(cls, username, password=None, email=None, first_name=None, last_name=None):
        """Get existing user or create new one if doesn't exist."""
        user = cls()
        user.username = username
        user.user_id = user._get_user_id_by_username(username)

        if user.user_id:
            # User exists, load details
            user._load_user_details()
        else:
            # Create new user
            if not all([password, email, first_name, last_name]):
                raise ValueError("Missing required fields for user creation.")

            user._password = password
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.user_id = user.admin.create_user(user._serialize_for_creation())

        return user

    def _get_user_id_by_username(self, username):
        """Get user ID by username, return None if not found."""
        try:
            return self.admin.get_user_id(username)
        except Exception:
            return None

    def _load_user_details(self):
        """Load user details from Keycloak."""
        if not self.user_id:
            raise ValueError("User ID not set")

        user_data = self.admin.get_user(self.user_id)
        self.username = user_data.get('username')
        self.email = user_data.get('email')
        self.first_name = user_data.get('firstName')
        self.last_name = user_data.get('lastName')

    def _serialize_for_creation(self):
        """Serialize user data for creation."""
        return {
            "email": self.email,
            "username": self.username,
            "credentials": [
                {
                    "value": self._password,
                    "type": "password",
                }
            ],
            "enabled": True,
            "realmRoles": ["user"],
            "firstName": self.first_name,
            "lastName": self.last_name,
            "emailVerified": True,
        }

    def as_dict(self):
        """Return user details as a dictionary."""
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
        }

    def set_password(self, password):
        """Set or update user password."""
        if not self.user_id:
            raise ValueError("User not initialized")

        self.admin.set_user_password(self.user_id, password, temporary=False)
        self._password = password

    def get_token(self, password=None):
        """Get token using provided password or stored password."""
        if not self.username:
            raise ValueError("Username not set")

        pwd = password or self._password
        if not pwd:
            raise ValueError("Password required for token generation")

        try:
            return self.client.token(self.username, pwd)
        except Exception as e:
            print(f"Exception getting token: {e}")
            return None

    def check_token(self, access_token):
        """Check if token is valid."""
        token_info = self.client.introspect(access_token)
        return token_info.get("active", False)

    def get_userinfo(self, access_token):
        """Get user info from token."""
        try:
            return self.client.userinfo(access_token)
        except Exception as e:
            print(f"Exception getting userinfo: {e}")
            return None

    def update(self, **kwargs):
        """Update user attributes."""
        if not self.user_id:
            raise ValueError("User not initialized")

        update_data = {}

        # Update local attributes and prepare update payload
        for key, value in kwargs.items():
            if key == 'email' and value:
                self.email = value
                update_data['email'] = value
            elif key == 'first_name' and value:
                self.first_name = value
                update_data['firstName'] = value
            elif key == 'last_name' and value:
                self.last_name = value
                update_data['lastName'] = value

        if update_data:
            self.admin.update_user(self.user_id, update_data)

    def delete(self):
        """Delete the user."""
        if not self.user_id:
            raise ValueError("User not initialized")

        self.admin.delete_user(self.user_id)
        self.user_id = None
