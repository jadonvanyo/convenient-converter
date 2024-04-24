import jwt, datetime, os
from flask import Flask, request
from flask_mysqldb import MySQL

# Config server so routes will access specific code
server = Flask(__name__)
# Connect app to MySQL DB
mysql = MySQL(server)

# Setup the configuration for server that will allow for connection to the database 
server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
server.config["MYSQL_PORT"] = int(os.environ.get("MYSQL_PORT"))

# Route for logging into the web application
@server.route("/login", methods=["POST"])
def login():
    # Get the entered username and password
    auth = request.authorization
    # Handle error if no user authentication can be found
    if not auth:
        return "missing credentials", 401

    # Create cursor to execute SQL queries
    cur = mysql.connection.cursor()
    # Check db for username and password
    res = cur.execute(
        "SELECT email, password FROM user WHERE email=%s", (auth.username,)
    )

    # If rows are returned, determine the email and password
    if res > 0:
        # Fetch the user data from the database
        user_row = cur.fetchone()
        email = user_row[0]
        password = user_row[1]

        # Determine if the username and password do NOT match what was entered
        if auth.username != email or auth.password != password:
            return "invalid credentials", 401
        # Generate a JWT token if the username and password matched
        else:
            return createJWT(auth.username, os.environ.get("JWT_SECRET"), True)
    # Invalid credentials if the user does not exist in the database
    else:
        return "invalid credentials", 401


@server.route("/validate", methods=["POST"])
def validate():
    """Validate a users JWT to determine if they are allowed to access the apps functions.

    Returns:
        _type_: _description_
    """
    # Get encoded JWT from the request headers for authorization
    encoded_jwt = request.headers["Authorization"]

    if not encoded_jwt:
        return "missing credentials", 401

    # Split the string to just access the encoded JWT
    encoded_jwt = encoded_jwt.split(" ")[1]

    # Attempt to decode the JWT
    try:
        decoded = jwt.decode(
            encoded_jwt, os.environ.get("JWT_SECRET"), algorithms=["HS256"]
        )
    except:
        return "not authorized", 403

    return decoded, 200


def createJWT(username, secret, authz):
    """Create a JSON Web Token (JWT) that encodes user information and authorization status.

    Args:
        username (str): The username of the user for whom the JWT is being created.
        secret (str): The secret key used to sign the JWT to ensure its security and integrity.
        authz (boolean): A boolean indicating whether the user has administrative privileges or not.

    Returns:
        str: A JSON Web Token encoded as a dictionary containing the user's data and authorization information.
    """
    return jwt.encode(
        {
            "username": username,
            "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=1),
            "iat": datetime.datetime.now(),
            "admin": authz,
        },
        secret,
        algorithm="HS256",
    )


if __name__ == "__main__":
    # Configure entry point to allow for application to listen to all public IPs
    server.run(host="0.0.0.0", port=5000)