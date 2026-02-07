from typing import Any

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError


class GeminiDrawProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        """
        Validate the credentials (API key) for the provider.

        Args:
            credentials: Dictionary containing api_key and optional base_url

        Raises:
            ToolProviderCredentialValidationError: If API key is missing or invalid
        """
        api_key = credentials.get("api_key")
        if not api_key:
            raise ToolProviderCredentialValidationError(
                "API Key is required. Please register at https://www.16api.com to get your API key."
            )
