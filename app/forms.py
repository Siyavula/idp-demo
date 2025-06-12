from wtforms import Form, StringField, PasswordField, validators
from app.models.user import KeycloakUser


class RegistrationForm(Form):
    username = StringField("Username", [validators.Length(min=4, max=25)])
    email = StringField(
        "Email address", [validators.DataRequired()]
    )
    first_name = StringField("First name", [validators.DataRequired()])
    last_name = StringField("Last name", [validators.DataRequired()])
    password = PasswordField(
        "Password",
        [
            validators.DataRequired(),
            validators.EqualTo("confirm", message="Passwords must match"),
        ],
    )
    confirm = PasswordField("Repeat password")

    def validate_username(self, field):
        try:
            if KeycloakUser.from_username(field.data):
                raise validators.ValidationError(
                    "Username already exists. Please choose another one."
                )
        except ValueError:
            # User does not exist, validation passes
            pass

    def save(self):
        user = KeycloakUser.create_new(
            username=self.username.data,
            password=self.password.data,
            email=self.email.data,
            first_name=self.first_name.data,
            last_name=self.last_name.data,
        )

        return user


class LoginForm(Form):
    username = StringField("Username", [validators.Length(min=4, max=25)])
    password = PasswordField("Password", [validators.DataRequired()])

    def validate(self):
        if not super().validate():
            return False

        try:
            user = KeycloakUser.from_username(self.username.data)
        except ValueError:
            self.username.errors.append("Invalid username or password.")
            return False

        if not user.get_token(self.password.data):
            self.username.errors.append("Invalid username or password.")
            return False

        return True

    def save(self):
        user = KeycloakUser.from_username(self.username.data)
        token = user.get_token(self.password.data)

        return user, token
