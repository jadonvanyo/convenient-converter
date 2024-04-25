import os, requests

def login(request):
    auth = request.authorization
    # No authorization parameters are found in the request
    if not auth:
        return None, ("missing credentials", 401)

    # Set the authorization to the username and password
    basicAuth = (auth.username, auth.password)

    # Make the HTTP call to the auth service
    response = requests.post(
        f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/login", auth=basicAuth
    )

    # Return the token and no error code if the status code is successful
    if response.status_code == 200:
        return response.text, None
    # Return the error if an unsuccessful error code shows
    else:
        return None, (response.text, response.status_code)