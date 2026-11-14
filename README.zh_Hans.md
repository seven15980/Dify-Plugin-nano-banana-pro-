# Nano Banana Pro

在 Dify 里通过 SteadyRouter 用 Nano Banana Pro（Gemini 3 Pro Image）文生图、改图。

SteadyRouter 是独立的 API 网关，与 Google 没有关联，也未获其背书。型号名只用来说明这个插件调用哪个型号。

从 0.1.x 升级来的？原来的 Key 照常能用。加一个 SteadyRouter 的 Key，能多得到这些：

- **这个插件里的型号全都能用**：Nano Banana 2.1、Gemini 3.1 Flash Image、Flash Lite Image，不受旧 Key 能用哪些型号的限制。
- **同一个 Key 出视频、用更多生图型号**：装 **SteadyRouter 图片和视频生成** 插件，就能用 Seedance、万相、Vidu 生成视频，还有 GPT Image、Seedream、Qwen Image、Flux。
- **少失败**：开着智能路由（新 Key 默认开），一个上游失败会自动换另一个重试。
- **新用户送体验额度**，可以先免费试试出图。

## 能做什么

- **文生图**：描述你想要的图片。
- **图生图**：最多 14 张参考图，说明怎么修改或融合。
- **型号**：Gemini 3 Pro（默认，画质更高）、Gemini 3.1 Flash（更快），以及较新的 Gemini 3 Pro Image、Gemini 3.1 Flash Image、Nano Banana 2.1、Gemini 3.1 Flash Lite Image。Flash Lite 只支持 1K，不管质量选什么都按 1K 生成。用旧版 Key 时，较新的型号取决于这把 Key 能用哪些。
- **宽高比**：自动、1:1、3:4、4:3、9:16、16:9。
- **质量**：1K、2K、4K。

## 配置

1. [注册 SteadyRouter](https://www.steadyrouter.com/sign-up)（新用户送体验额度，可以先免费试试出图），在控制台打开 **API Keys** → **Create API Key**。
2. 在 Dify 打开 **工具** → **Nano Banana Pro** → **授权**，把 Key 粘贴到 **SteadyRouter API Key**，旧版字段留空。
3. 把 **AI 图像生成** 工具加到工作流或 Agent 里。

## 使用说明

- 图片以文件返回，由 Dify 保存，不会把会过期的链接交给你。
- 型号、宽高比、质量在工具设置里选。质量越高越贵。
- 当前价格见 [模型广场](https://www.steadyrouter.com/pricing)。失败的请求不扣费。
- 工作流里给工具节点留几分钟超时时间。
- Dify 新版 **Agents（beta）** 暂时收不了工具返回的文件：图其实已经生成、也扣了费，界面却显示「Action failed」和一串乱码。Dify 修好之前，请在工作流、Chatflow 或经典 Agent 应用里用这个工具。

## 需要什么

- 需要 SteadyRouter API Key，以及能访问 `api.steadyrouter.com` 的出站 HTTPS。
- 文件通过网关返回的存储链接下载：只走 HTTPS，不带你的 Key，私有网络地址一律拒绝。

## 链接

- 源码：https://github.com/seven15980/Dify-Plugin-nano-banana-pro-
- 文档：https://www.steadyrouter.com/site/docs.html
- 隐私：见 [PRIVACY.md](PRIVACY.md)
- 联系：support@steadyrouter.com
