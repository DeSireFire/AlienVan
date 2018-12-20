import onedrivesdk
import logging
import json
from time import time
from alienVan.appConfig import *

## Saving and Loading a Session

# session保存
def save_session(client):
    auth_provider = onedrivesdk.AuthProvider(
                    http_provider,
                    client_id,
                    scopes)

    auth_provider.authenticate(
        code,
        redirect_uri,
        client_secret)

    # Save the session for later
    auth_provider.save_session()

def load_session(client):
    #### Next time you start the app ####
    auth_provider = onedrivesdk.AuthProvider(
                    http_provider,
                    client_id,
                    scopes)
    auth_provider.load_session()
    auth_provider.refresh_token()
    client = onedrivesdk.OneDriveClient(
                base_url,
                auth_provider,
                http_provider)