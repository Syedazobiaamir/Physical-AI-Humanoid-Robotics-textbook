"""
OAuth integration for Google and GitHub authentication
"""
from typing import Optional, Dict
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

# OAuth configurations
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USER_INFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"

GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
GITHUB_AUTH_URL = "https://github.com/login/oauth/authorize"
GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"
GITHUB_USER_INFO_URL = "https://api.github.com/user"


class OAuthProvider:
    """Base OAuth provider class"""

    def __init__(self, client_id: str, client_secret: str, auth_url: str,
                 token_url: str, user_info_url: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.auth_url = auth_url
        self.token_url = token_url
        self.user_info_url = user_info_url

    def get_authorization_url(self, redirect_uri: str, state: str) -> str:
        """Generate OAuth authorization URL"""
        raise NotImplementedError

    async def get_access_token(self, code: str, redirect_uri: str) -> Optional[str]:
        """Exchange authorization code for access token"""
        raise NotImplementedError

    async def get_user_info(self, access_token: str) -> Optional[Dict]:
        """Get user information using access token"""
        raise NotImplementedError


class GoogleOAuth(OAuthProvider):
    """Google OAuth provider"""

    def __init__(self):
        super().__init__(
            GOOGLE_CLIENT_ID,
            GOOGLE_CLIENT_SECRET,
            GOOGLE_AUTH_URL,
            GOOGLE_TOKEN_URL,
            GOOGLE_USER_INFO_URL
        )

    def get_authorization_url(self, redirect_uri: str, state: str) -> str:
        """Generate Google OAuth authorization URL"""
        params = {
            "client_id": self.client_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": "openid email profile",
            "state": state,
            "access_type": "offline",
            "prompt": "consent"
        }
        param_str = "&".join([f"{k}={v}" for k, v in params.items()])
        return f"{self.auth_url}?{param_str}"

    async def get_access_token(self, code: str, redirect_uri: str) -> Optional[str]:
        """Exchange Google authorization code for access token"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.token_url,
                data={
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "code": code,
                    "grant_type": "authorization_code",
                    "redirect_uri": redirect_uri
                }
            )
            if response.status_code == 200:
                data = response.json()
                return data.get("access_token")
        return None

    async def get_user_info(self, access_token: str) -> Optional[Dict]:
        """Get Google user information"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self.user_info_url,
                headers={"Authorization": f"Bearer {access_token}"}
            )
            if response.status_code == 200:
                return response.json()
        return None


class GitHubOAuth(OAuthProvider):
    """GitHub OAuth provider"""

    def __init__(self):
        super().__init__(
            GITHUB_CLIENT_ID,
            GITHUB_CLIENT_SECRET,
            GITHUB_AUTH_URL,
            GITHUB_TOKEN_URL,
            GITHUB_USER_INFO_URL
        )

    def get_authorization_url(self, redirect_uri: str, state: str) -> str:
        """Generate GitHub OAuth authorization URL"""
        params = {
            "client_id": self.client_id,
            "redirect_uri": redirect_uri,
            "scope": "user:email",
            "state": state
        }
        param_str = "&".join([f"{k}={v}" for k, v in params.items()])
        return f"{self.auth_url}?{param_str}"

    async def get_access_token(self, code: str, redirect_uri: str) -> Optional[str]:
        """Exchange GitHub authorization code for access token"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.token_url,
                data={
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "code": code,
                    "redirect_uri": redirect_uri
                },
                headers={"Accept": "application/json"}
            )
            if response.status_code == 200:
                data = response.json()
                return data.get("access_token")
        return None

    async def get_user_info(self, access_token: str) -> Optional[Dict]:
        """Get GitHub user information"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self.user_info_url,
                headers={"Authorization": f"token {access_token}"}
            )
            if response.status_code == 200:
                return response.json()
        return None


def get_oauth_provider(provider: str) -> Optional[OAuthProvider]:
    """Get OAuth provider instance by name"""
    providers = {
        "google": GoogleOAuth,
        "github": GitHubOAuth
    }
    provider_class = providers.get(provider.lower())
    if provider_class:
        return provider_class()
    return None
