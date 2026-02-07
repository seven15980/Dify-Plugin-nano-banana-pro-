# 🔄 从 Builtin Tool 迁移到 Plugin 系统

## 重要说明 ⚠️

你的插件目前是作为 **Builtin Tool** 开发的（旧系统），但从 **Dify v1.0.0** (2025年2月) 开始，所有工具已迁移到新的 **Plugin 系统**。

在发布前，需要进行代码迁移。

## 主要变更对比

### 1. Import 语句变更

**❌ 旧系统 (Builtin Tool):**
```python
from core.tools.builtin_tool.tool import BuiltinTool
from core.tools.builtin_tool.provider import BuiltinToolProviderController
from core.tools.entities.tool_entities import ToolInvokeMessage
from core.file.file_manager import download
```

**✅ 新系统 (Plugin):**
```python
from dify_plugin import Tool, ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError
from dify_plugin.entities.tool import ToolInvokeMessage
# 注意：文件处理方式可能不同，需要查看官方文档
```

### 2. 基类变更

**❌ 旧系统:**
```python
class GeminiDrawProvider(BuiltinToolProviderController):
    def _validate_credentials(self, user_id: str, credentials: dict[str, Any]):
        pass

class GenerateImageTool(BuiltinTool):
    def _invoke(self, user_id: str, tool_parameters: dict[str, Any], ...):
        ...
```

**✅ 新系统:**
```python
class GeminiDrawProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        # 注意：没有 user_id 参数
        if not credentials.get("gemini_api_key"):
            raise ToolProviderCredentialValidationError("API Key is required")

class GenerateImageTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        # 参数签名可能有变化
        ...
```

### 3. 项目结构变更

**❌ 旧系统（嵌入 Dify 源码）:**
```
dify/api/core/tools/builtin_tool/providers/gemini_draw/
├── gemini_draw.py
├── gemini_draw.yaml
└── tools/
    ├── generate_image.py
    ├── generate_image.yaml
    ├── image_to_image.py
    └── image_to_image.yaml
```

**✅ 新系统（独立插件）:**
```
gemini-draw/
├── main.py              # 新增：插件入口
├── manifest.yaml        # 新增：插件清单
├── README.md
├── privacy.md
├── pyproject.toml       # 新增：Python 项目配置
├── requirements.txt     # 新增：依赖声明
├── provider/
│   ├── gemini_draw.yaml
│   └── gemini_draw.py   # 需要修改 import
├── tools/
│   ├── generate_image.yaml
│   ├── generate_image.py    # 需要修改 import
│   ├── image_to_image.yaml
│   └── image_to_image.py    # 需要修改 import
└── _assets/
    └── icon.svg
```

## 🔨 迁移步骤

### 步骤 1: 创建插件入口文件

创建 `main.py`：
```python
from dify_plugin import DifyPluginEnv, Plugin

plugin = Plugin(DifyPluginEnv())

if __name__ == "__main__":
    plugin.run()
```

### 步骤 2: 创建项目配置

创建 `pyproject.toml`：
```toml
[project]
name = "nano-banana-pro"
version = "0.1.0"
description = "Nano Banana Pro - Gemini Image Generation and Transformation Plugin"
authors = [
    {name = "16api.com", email = "contact@16api.com"}
]
requires-python = ">=3.12"
dependencies = [
    "dify_plugin>=0.3.0,<0.5.0",
    "requests>=2.31.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

创建 `requirements.txt`：
```
dify_plugin>=0.3.0,<0.5.0
requests>=2.31.0
```

### 步骤 3: 修改 Provider 代码

修改 `provider/gemini_draw.py`：

```python
from typing import Any
from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError


class GeminiDrawProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        # 验证 API Key 是否存在
        if not credentials.get("gemini_api_key"):
            raise ToolProviderCredentialValidationError(
                "Gemini API Key is required. Get one at https://ai.google.dev/"
            )
```

### 步骤 4: 修改 Tool 代码

修改 `tools/generate_image.py` 和 `tools/image_to_image.py`：

**关键修改：**
1. 修改 import 语句（见上方对比）
2. 修改基类为 `Tool`
3. 修改 `_invoke` 方法签名（移除 `user_id` 等参数）
4. 文件处理逻辑可能需要调整（查看官方文档）

**示例（简化版）：**
```python
from collections.abc import Generator
from typing import Any
import requests
import base64

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage


class GenerateImageTool(Tool):
    def _invoke(
        self,
        tool_parameters: dict[str, Any]
    ) -> Generator[ToolInvokeMessage, None, None]:
        # 获取 runtime 中的凭据
        api_key = self.runtime.credentials.get("gemini_api_key")

        # 你的图像生成逻辑...
        prompt = tool_parameters.get("prompt", "")

        # API 调用
        response = self._call_gemini_api(api_key, prompt)

        # 返回结果
        yield self.create_blob_message(
            blob=image_data,
            meta={'mime_type': 'image/jpeg'}
        )

    def _call_gemini_api(self, api_key: str, prompt: str):
        # 你的 API 调用逻辑
        pass
```

### 步骤 5: 更新 manifest.yaml

确保 manifest.yaml 包含所有必要字段（已在前面创建）。

### 步骤 6: 测试插件

```bash
# 安装依赖
cd gemini-draw-plugin
pip install -r requirements.txt

# 本地测试（可能需要配置 .env）
python main.py
```

## ⚠️ 注意事项

### 1. 文件处理差异

你的代码中使用了：
```python
from core.file.file_manager import download
img_binary = download(image_file)
```

在新插件系统中，文件处理方式可能不同。建议：
- 查看官方 Gemini Image 插件的实现
- 参考 `dify_plugin` 文档中的文件处理 API
- 可能需要使用不同的方法处理上传的图片

### 2. 你的特殊修复代码

你的开发文档中提到的几个修复：

**修复 1: File 序列化问题**
- 这是 builtin tool 系统的问题
- 新插件系统应该已经解决这个问题
- **不需要**修改 `tool_parameter_cache.py` 和 `configuration.py`

**修复 2: API 响应解析（驼峰命名）**
- 这个修复**仍然需要**保留
- 继续使用兼容两种命名的代码：
  ```python
  inline_data = part.get("inlineData") or part.get("inline_data")
  ```

**修复 3: INTERNAL_FILES_URL vs FILES_URL**
- 这是 Dify 部署配置问题，不是插件代码问题
- 插件代码中**不需要**处理这个

### 3. 官方已有类似插件

**重要发现：** Dify 官方插件中已经有 `gemini_image` 插件了！

你的选择：
1. **贡献改进** - 如果你的实现更好，可以提 PR 改进官方插件
2. **发布独立插件** - 如果功能差异明显，可以发布为独立插件（需要明确差异点）
3. **内部使用** - 作为自己的私有插件使用

建议先对比功能：
- 官方插件：https://github.com/langgenius/dify-official-plugins/tree/main/tools/gemini_image
- 你的插件特色功能是什么？

## 📚 参考资源

- **官方 Gemini Image 插件**: https://github.com/langgenius/dify-official-plugins/tree/main/tools/gemini_image
- **Plugin SDK 文档**: https://docs.dify.ai/plugins/
- **Plugin SDK GitHub**: https://github.com/langgenius/dify-plugin-sdks
- **Dify Plugins 仓库**: https://github.com/langgenius/dify-plugins

## 下一步

1. **评估**: 对比你的插件与官方 gemini_image 插件的功能差异
2. **决定**: 选择贡献、独立发布或内部使用
3. **迁移**: 按照本指南迁移代码到新插件系统
4. **测试**: 充分测试所有功能
5. **发布**: 按照 PUBLISHING_GUIDE.md 发布

需要帮助时，随时联系 Dify 社区！
