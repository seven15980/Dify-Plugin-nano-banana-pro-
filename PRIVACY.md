# Privacy

This plugin sends each request to one of two services, depending on which key you configured. It never sends to both.

**With a SteadyRouter API key** (the default for new users; used whenever this key is filled in): requests go to SteadyRouter (`api.steadyrouter.com`). The legacy key, if you also have one, is not sent anywhere.

**With only the legacy key from version 0.1.x**: requests go to the same legacy service as before (`www.16api.com`). Nothing is sent to SteadyRouter.

**What is sent**: your prompts, any reference images you provide, the settings you choose, and the API key for that service to identify your account.

**Who receives it**: the service your key belongs to, which forwards the request to the upstream provider that serves the model. SteadyRouter's own handling of your data is described in its [Privacy Policy](https://www.steadyrouter.com/site/privacy.html). The legacy service has its own terms.

**Other requests the plugin makes**: on the SteadyRouter route it downloads the finished image from the storage link in the reply, if there is one, without your key.

**What the plugin stores**: nothing. Finished files are handed straight to Dify, which stores them. The plugin keeps no copy, collects no analytics, and does not log your keys. Dify stores the keys in its own credential system.

SteadyRouter is an independent API gateway, not affiliated with Google.

Questions: support@steadyrouter.com
