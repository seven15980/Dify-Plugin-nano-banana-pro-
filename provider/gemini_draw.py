from typing import Any

from dify_plugin import ToolProvider
from dify_plugin.errors.model import CredentialsValidateFailedError
from srclient import SRClient, SRError


class GeminiDrawProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        """
        Both key fields are optional in the form, so "at least one" is enforced here. Only the SteadyRouter key is
        checked over the network. The legacy key is never sent anywhere from this method, as in 0.1.x.

        Raises:
            CredentialsValidateFailedError: If no key is filled in, or the SteadyRouter key is refused. Dify shows this
                type's message as it is. ToolProviderCredentialValidationError reaches the user as a whole traceback.
        """
        steadyrouter_key = (credentials.get("steadyrouter_api_key") or "").strip()
        if steadyrouter_key:
            try:
                SRClient(steadyrouter_key, user_agent="steadyrouter-dify").check_key()
            except SRError as exc:
                raise CredentialsValidateFailedError(str(exc)) from exc
            return
        if not (credentials.get("api_key") or "").strip():
            raise CredentialsValidateFailedError("Add your SteadyRouter API key. 请填写 SteadyRouter API Key。")
