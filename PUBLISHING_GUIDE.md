# 📦 Nano Banana Pro Plugin - 发布指南

本指南将帮助你将 Nano Banana Pro 插件发布到 Dify Marketplace。

## 📋 发布前检查清单

- [ ] 插件在本地测试通过
- [ ] 所有文件准备齐全（见下方文件清单）
- [ ] README.md 已更新（包含作者信息和仓库链接）
- [ ] privacy.md 已审阅
- [ ] manifest.yaml 版本号正确
- [ ] 图标文件已准备（icon.svg）

## 📁 必需文件清单

```
nano-banana-pro/
├── manifest.yaml              ✅ 插件清单
├── README.md                  ✅ 插件说明
├── privacy.md                 ✅ 隐私政策
├── provider/
│   ├── gemini_draw.yaml       ✅ Provider 配置
│   └── gemini_draw.py         ✅ Provider 实现
├── tools/
│   ├── __init__.py            ✅
│   ├── generate_image.yaml    ✅ 文生图配置
│   ├── generate_image.py      ✅ 文生图实现
│   ├── image_to_image.yaml    ✅ 图生图配置
│   └── image_to_image.py      ✅ 图生图实现
└── _assets/
    └── icon.svg               ✅ 插件图标
```

## 🚀 发布步骤

### 步骤 1: 安装 Dify Plugin CLI

```bash
pip install dify-plugin
```

### 步骤 2: 更新个人信息

编辑以下文件，替换占位符：

1. **manifest.yaml**
   ```yaml
   author: 16api.com  # ✅ 已更新
   name: nano_banana_pro  # ✅ 已更新
   ```

2. **README.md**
   - ✅ 作者信息已更新
   - 可以添加 GitHub 仓库 URL（如果有）

3. **privacy.md**
   - ✅ 联系方式已更新

### 步骤 3: 打包插件

```bash
cd /path/to/gemini-draw-plugin
dify plugin package .
```

这会生成 `.difypkg` 文件，例如：`nano_banana_pro-0.1.0.difypkg`

### 步骤 4: 本地测试（可选但推荐）

在发布前先在本地 Dify 实例测试：

1. 登录你的 Dify 实例
2. 进入 **工作室** → **插件**
3. 点击 **安装插件** → **上传本地文件**
4. 选择生成的 `.difypkg` 文件
5. 测试两个工具是否正常工作

### 步骤 5: Fork Dify Plugins 仓库

前往 GitHub 仓库并 Fork：

- **社区插件**（推荐）: https://github.com/langgenius/dify-plugins
- **官方插件**: https://github.com/langgenius/dify-official-plugins

```bash
# Clone 你的 fork
git clone https://github.com/YOUR_USERNAME/dify-plugins.git
cd dify-plugins
```

### 步骤 6: 创建插件目录结构

```bash
# 创建组织/插件目录
mkdir -p 16api/nano-banana-pro

# 复制所有文件到新目录
cp -r /path/to/nano-banana-pro/* 16api/nano-banana-pro/

# 复制打包好的 .difypkg 文件
cp /path/to/nano_banana_pro-0.1.0.difypkg 16api/nano-banana-pro/
```

最终目录结构：
```
dify-plugins/
└── 16api/
    └── nano-banana-pro/
        ├── nano_banana_pro-0.1.0.difypkg   # 打包文件
        ├── manifest.yaml
        ├── README.md
        ├── privacy.md
        ├── provider/
        ├── tools/
        └── _assets/
```

### 步骤 7: 提交 Pull Request

```bash
# 创建新分支
git checkout -b add-nano-banana-pro-plugin

# 添加文件
git add 16api/nano-banana-pro

# 提交
git commit -m "feat: add Nano Banana Pro plugin

- Text-to-Image generation
- Image-to-Image transformation
- Multi-language support (EN/CN)
- Multiple quality and aspect ratio options"

# 推送到你的 fork
git push origin add-nano-banana-pro-plugin
```

### 步骤 8: 在 GitHub 创建 PR

1. 访问你的 fork 仓库页面
2. 点击 **Compare & pull request**
3. 填写 PR 信息：

**标题格式**：
```
feat: Add Nano Banana Pro - AI Image Generation Plugin
```

**PR 描述模板**：
```markdown
## Plugin Information

- **Name**: Nano Banana Pro
- **Type**: Tool
- **Author**: 16api.com
- **Version**: 0.1.0

## Description

Nano Banana Pro is a powerful AI image generation plugin powered by Google Gemini API.

**Features:**
- Text-to-Image generation with customizable settings
- Image-to-Image transformation
- Multiple aspect ratios (1:1, 3:4, 4:3, 9:16, 16:9)
- Multiple quality levels (SD, HD, 4K)
- Multi-language support (English & Chinese)

## Testing

- [x] Plugin installed successfully
- [x] Text-to-image generation works
- [x] Image-to-image transformation works
- [x] All configurations tested
- [x] Error handling verified

## Screenshots

[Add screenshots of your plugin in action]

## Checklist

- [x] README.md included with contact information
- [x] Privacy policy (privacy.md) included
- [x] .difypkg file generated and included
- [x] Icon provided (_assets/icon.svg)
- [x] All YAML files properly formatted
- [x] Tested locally before submission

## Additional Notes

This plugin includes several important fixes:
- Compatible API response parsing (camelCase/snake_case)
- Proper file handling with Dify's download() function
- Secure credential management
```

### 步骤 9: 等待审核

Dify 团队会审核你的 PR：

- 通常需要 **几天到几周** 时间
- 审核人员可能会提出修改建议
- 根据反馈进行调整并更新 PR
- 审核通过后，插件会自动上架到 Marketplace

### 步骤 10: 插件更新（未来）

当需要更新插件时：

1. 修改 `manifest.yaml` 中的版本号（例如：0.1.0 → 0.1.1）
2. 重新打包：`dify plugin package .`
3. 将新的 `.difypkg` 文件添加到插件目录
4. 更新 README.md 记录变更
5. 提交新的 PR（标题：`feat: Update Nano Banana Pro to v0.1.1`）

## 🎯 发布到其他渠道

### 方式 1: GitHub 仓库直接安装

用户可以通过你的 GitHub 仓库链接直接安装：

1. 创建独立的 GitHub 仓库存放你的插件
2. 用户在 Dify 中通过 **从 GitHub 安装** 功能
3. 输入你的仓库 URL 即可安装

### 方式 2: 本地文件分发

适合内部使用或测试：

1. 分享 `.difypkg` 文件
2. 用户通过 **上传本地文件** 安装

## ❓ 常见问题

### Q1: PR 被拒绝了怎么办？

查看审核人员的反馈，通常原因包括：
- 代码质量问题
- 缺少必要文档
- 隐私政策不完整
- 插件功能与现有插件重复

根据反馈修改后重新提交。

### Q2: 如何加快审核速度？

- 确保所有文档完整且清晰
- 提供详细的测试说明
- 包含使用截图或视频
- 代码质量高，注释充分

### Q3: 插件被接受后可以修改吗？

可以！提交新版本的 PR，增加版本号即可。

### Q4: 是否需要签署协议？

Dify Plugins 仓库使用 Apache-2.0 许可证，你的贡献会自动遵循该许可证。

## 📞 获取帮助

- **Dify 文档**: https://docs.dify.ai/
- **Dify 社区**: https://github.com/langgenius/dify/discussions
- **插件开发指南**: https://docs.dify.ai/plugins/
- **安全问题**: security@dify.ai

## 🎉 成功发布后

恭喜！你的插件现在可以：

- ✅ 在 Dify Marketplace 被所有用户发现
- ✅ 通过 Dify UI 一键安装
- ✅ 自动获得更新推送（当你发布新版本时）
- ✅ 被社区使用和反馈

记得在社交媒体分享你的成果！ 🚀
