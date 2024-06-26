import os, requests

def token(request):
    """Validate a user token"""
    # Determine if authorization is in the header
    if not "Authorization" in request.headers:
        return None, ("missing credentials", 401)
    
    # Establish the token from the header
    token = request.headers["Authorization"]
    
    # Determine if the token exists
    if not token:
        return None, ("missing credentials", 401)
    
    # Pass the token to the validation service
    response = requests.post(
        f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/validate",
        headers={"Authorization": token},
    )
    
    # Determine if the token could be successfully validated
    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)