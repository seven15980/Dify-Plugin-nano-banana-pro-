# Nano Banana Pro - AI Image Generation Plugin

![Version](https://img.shields.io/badge/version-0.1.0-blue)
![License](https://img.shields.io/badge/license-Apache--2.0-green)
![Author](https://img.shields.io/badge/author-16api.com-orange)

## 📖 Overview

Nano Banana Pro is a powerful Dify plugin that leverages Google's Gemini AI for image generation and transformation. It provides a unified **AI Image Generation** tool with dual capabilities:

**One Tool, Two Modes:**
1. **Text-to-Image Mode** - Generate images from text descriptions only (no input images required)
2. **Image-to-Image Mode** - Transform or fuse up to 14 reference images with text instructions

## ✨ Features

- 🎨 **Dual Mode Operation** - Text-only or image transformation in one tool
- 📐 **Multiple Aspect Ratios** - 1:1, 3:4, 4:3, 9:16, 16:9, or Auto
- 🖼️ **Quality Levels** - 1K (Standard), 2K (HD), 4K (Ultra HD)
- 🔄 **Multi-Image Fusion** - Combine up to 14 images
- 🌐 **Multi-Language** - English & Chinese interface
- ⚡ **Gemini Powered** - Fast and high-quality generation

## 🚀 Usage

### Mode 1: Text-to-Image (文生图)

Generate images from text descriptions without uploading any images:

```
Tool: AI Image Generation
Input Images: [Leave empty]
Description: "A serene mountain landscape at sunset with aurora borealis"
Aspect Ratio: 16:9
Quality: 2K
```

### Mode 2: Image-to-Image (图生图)

Transform or edit existing images:

```
Tool: AI Image Generation
Input Images: [Upload 1-14 images]
Instructions: "Make it look like a watercolor painting, add falling snow"
Aspect Ratio: auto
Quality: 2K
```

## 🔧 Configuration

1. **Install the plugin** in Dify
2. **Register at 16api.com**
   - Visit: https://www.16api.com
   - Sign up for a free account
   - Get your API Key from the dashboard
3. **Configure the plugin**
   - Open plugin settings in Dify
   - Enter your API Key from 16api.com
   - Base URL is pre-configured (no need to change)
4. **Start using!** Create workflows with the AI Image Generation tool

## 📋 Requirements

- Dify Platform v1.0.0+
- 16api.com account (free registration at https://www.16api.com)
- API Key from 16api.com dashboard

## 🐛 Known Issues & Fixes

This plugin includes fixes for several issues discovered during development:

- ✅ API response parsing (supports both camelCase and snake_case)
- ✅ File serialization handling
- ✅ Proper image URL generation

For detailed development notes, see the development documentation.

## 📝 License

Apache-2.0

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

- Author: 16api.com
- Website: https://16api.com
- Repository: https://github.com/seven15980/Dify-Plugin-nano-banana-pro-
- Issues: https://github.com/seven15980/Dify-Plugin-nano-banana-pro-/issues

## 🙏 Acknowledgments

Built with:
- Google Gemini AI
- Dify Platform
