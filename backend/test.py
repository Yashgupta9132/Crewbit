## Single user


# import msal, requests

# CLIENT_ID = "a529c80a-cf8b-4075-aa81-fd71826a47c8"
# AUTHORITY = "https://login.microsoftonline.com/common"
# SCOPES = ["Mail.Read"]

# def get_token():
#     app = msal.PublicClientApplication(CLIENT_ID, authority=AUTHORITY)
#     result = app.acquire_token_interactive(scopes=SCOPES)
#     if "access_token" not in result:
#         raise RuntimeError(f"Login failed: {result}")
#     print("Login successful!")
#     return result["access_token"]

# def fetch_emails(access_token, top=5):
#     endpoint = (
#         "https://graph.microsoft.com/v1.0/me/messages"
#         f"?$top={top}&$select=subject,from,receivedDateTime,bodyPreview"
#         "&$orderby=receivedDateTime%20desc"
#     )
#     headers = {"Authorization": f"Bearer {access_token}"}
#     r = requests.get(endpoint, headers=headers)
#     if r.status_code != 200:
#         raise RuntimeError(f"Graph error {r.status_code}: {r.text}")
#     return r.json().get("value", [])

# if __name__ == "__main__":
#     token = get_token()
#     emails = fetch_emails(token)
#     for mail in emails:
#         print(f"\n {mail['subject']}")
#         print(f"   From: {mail['from']['emailAddress']['address']}")
#         print(f"   Date: {mail['receivedDateTime']}")
#         print(f"   Preview: {mail['bodyPreview'][:80]}...")
















# import msal

# CLIENT_ID = "a529c80a-cf8b-4075-aa81-fd71826a47c8"
# AUTHORITY = "https://login.microsoftonline.com/common"
# SCOPE = ["Mail.Read"]

# app = msal.PublicClientApplication(CLIENT_ID, authority=AUTHORITY)

# # Get token interactively using device code
# result = app.acquire_token_interactive(scopes=SCOPE)

# if "access_token" in result:
#     print("✅ Login successful!")
#     print(result["access_token"])
# else:
#     print("❌ Login failed:", result)




































from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, JSONResponse
from msal import ConfidentialClientApplication
import uvicorn
import requests

# ===== Azure AD App Config (Fill in yours) =====
CLIENT_ID = "69542bee-ac05-4410-8854-26c108bc2872"
CLIENT_SECRET = "AIm8Q~ZoXTvGRSosoCS.ftZ75wCvIWiqKiAeHcL7"
TENANT_ID = "c57c02f0-f2ee-4fad-b998-31adfb0d722b"
REDIRECT_URI = "http://localhost:9002/auth/redirect"
SCOPES = ["User.Read", "Mail.Read"]

app = FastAPI()

# MSAL client setup
msal_app = ConfidentialClientApplication(
    CLIENT_ID,
    authority=f"https://login.microsoftonline.com/{TENANT_ID}",
    client_credential=CLIENT_SECRET
)

# Root endpoint redirects immediately to login
@app.get("/")
def root():
    return RedirectResponse(url="/ms/login")

@app.get("/me")
def me_info():
    flow = getattr(app.state, "flow", None)
    if not flow:
        return JSONResponse({"error": "No auth flow found. Go to /ms/login to start."})
    result = msal_app.acquire_token_by_auth_code_flow(flow, dict(request.query_params))
    if "access_token" in result:
        headers = {"Authorization": f"Bearer {result['access_token']}"}
        resp = requests.get("https://graph.microsoft.com/v1.0/me", headers=headers)
        return resp.json()
    else:
        return JSONResponse({"error": result.get("error_description", "Login failed")})


# Step 1: Start authentication flow
@app.get("/ms/login")
def login():
    flow = msal_app.initiate_auth_code_flow(
        SCOPES,
        redirect_uri=REDIRECT_URI
    )
    app.state.flow = flow
    return RedirectResponse(flow["auth_uri"])

# Step 2: Handle Azure redirect with auth code
@app.get("/auth/redirect")
def authorized(request: Request):
    flow = getattr(app.state, "flow", None)
    if not flow:
        return JSONResponse({"error": "No auth flow found. Start login from /ms/login."})

    result = msal_app.acquire_token_by_auth_code_flow(
        flow,
        dict(request.query_params)
    )

    if "access_token" in result:
        headers = {"Authorization": f"Bearer {result['access_token']}"}
        
        graph_resp = requests.get(
                "https://graph.microsoft.com/v1.0/me",
                headers=headers
                )
        print("Graph API status:", graph_resp.status_code)
        print("Graph API text:", graph_resp.text)

        
        # Handle possible 403 or non-JSON errors gracefully
        try:
            emails = graph_resp.json().get("value", [])
            return {"emails": [
                {
                    "subject": e.get("subject"),
                    "from": e.get("from", {}).get("emailAddress", {}).get("address"),
                    "date": e.get("receivedDateTime"),
                    "preview": e.get("bodyPreview")
                } for e in emails
            ]}
        except Exception as e:
            return JSONResponse({
                "error": "Graph API did not return JSON.",
                "status_code": graph_resp.status_code,
                "response": graph_resp.text
            })

    else:
        print("MSAL token acquisition failed:", result)
        return JSONResponse({"error": result.get("error_description", "Login failed")})

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=9002)