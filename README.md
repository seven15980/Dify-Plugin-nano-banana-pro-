# Nano Banana Pro

Generate and edit images in Dify with Nano Banana Pro (Gemini 3 Pro Image), through SteadyRouter.

SteadyRouter is an independent API gateway. It is not affiliated with or endorsed by Google. The model name only says which model this plugin calls.

Upgrading from 0.1.x? Nothing changes: your existing key keeps working the way it did, and adding a SteadyRouter key is optional.

## What it does

- **Text to image**: describe the picture you want.
- **Image to image**: give up to 14 reference images and say how to change or combine them.
- **Models**: Gemini 3 Pro (default, higher quality), Gemini 3.1 Flash (faster), or the newer Gemini 3 Pro Image, Gemini 3.1 Flash Image, Nano Banana 2.1 and Gemini 3.1 Flash Lite Image. Flash Lite only supports 1K, so it always uses 1K whatever the quality setting says. With a legacy key, the newer models depend on what that key can use.
- **Aspect ratio**: auto, 1:1, 3:4, 4:3, 9:16 or 16:9.
- **Quality**: 1K, 2K or 4K.

## Setup

1. [Create a SteadyRouter account](https://www.steadyrouter.com/sign-up), add funds, and open **API Keys** → **Create API Key** in the console.
2. In Dify, open **Tools** → **Nano Banana Pro** → **Authorize** and paste the key into **SteadyRouter API Key**. Leave the legacy field empty.
3. Add the **AI Image Generation** tool to your workflow or agent.

## Usage notes

- Images come back as files, which Dify stores. Links that expire are never passed on to you.
- Choose the model, aspect ratio and quality in the tool's settings. Higher quality costs more.
- Current prices are on [Model Square](https://www.steadyrouter.com/pricing). Requests that fail are not charged.
- In a workflow, allow the tool node several minutes before it times out.

## Requirements

- Needs a SteadyRouter API key and outbound HTTPS access to `api.steadyrouter.com`.
- Files are downloaded from the storage links the gateway returns, over HTTPS, without your key. Addresses on private networks are refused.

## Links

- Source code: https://github.com/seven15980/Dify-Plugin-nano-banana-pro-
- Docs: https://www.steadyrouter.com/site/docs.html
- Privacy: see [PRIVACY.md](PRIVACY.md)
- Contact: support@steadyrouter.com
