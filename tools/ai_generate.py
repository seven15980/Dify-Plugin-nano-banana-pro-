from collections.abc import Generator
from typing import Any
import requests
import base64

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage


class AiGenerate(Tool):
    """
    AI Image Generation tool using Gemini 3 Pro Image API
    - Text-to-Image: Generate images from text descriptions (no input images required)
    - Image-to-Image: Transform and fuse multiple images based on text instructions
    Supports up to 14 reference images (6 high-fidelity objects + 5 persons + 3 others).
    """

    # Gemini 3 Pro Image 的限制
    MAX_TOTAL_IMAGES = 14
    MAX_HIGH_FIDELITY_OBJECTS = 6
    MAX_PERSON_IMAGES = 5

    def _invoke(
        self,
        tool_parameters: dict[str, Any],
    ) -> Generator[ToolInvokeMessage, None, None]:
        """
        Invoke the AI image generation tool with dual mode support (text-to-image and image-to-image)

        Args:
            tool_parameters: Tool parameters including image_files, prompt, aspect_ratio, image_size

        Yields:
            ToolInvokeMessage: Text messages for progress/errors and blob message for the generated image
        """

        # 【调试日志】打印参数信息，帮助定位迭代中文件丢失问题
        import logging
        logging.warning(f"[DEBUG image_to_image] tool_parameters keys: {list(tool_parameters.keys())}")
        logging.warning(f"[DEBUG image_to_image] image_files type: {type(tool_parameters.get('image_files'))}")
        image_files_debug = tool_parameters.get('image_files')
        if isinstance(image_files_debug, list):
            logging.warning(f"[DEBUG image_to_image] image_files length: {len(image_files_debug)}")
            for i, f in enumerate(image_files_debug):
                logging.warning(f"[DEBUG image_to_image] file[{i}] type: {type(f)}, value: {f}")
        else:
            logging.warning(f"[DEBUG image_to_image] image_files value: {image_files_debug}")

        # 【关键修复】立即提取并移除 image_files，避免 JSON 序列化问题
        # Dify 会缓存 tool_parameters 到 Redis，File 对象无法被序列化
        image_files = tool_parameters.pop('image_files', None)

        # 处理 image_files 的各种格式，统一转换为列表
        valid_files = []

        if image_files is not None:
            # Normalize to list
            if not isinstance(image_files, list):
                if isinstance(image_files, str):
                    # String is invalid, ignore (allow text-to-image mode)
                    image_files = []
                else:
                    # Single file object, convert to list
                    image_files = [image_files]

            # Filter valid file objects (objects with blob/read method or similar)
            valid_files = [
                f for f in image_files
                if hasattr(f, 'blob') or hasattr(f, 'read') or hasattr(f, '__bytes__')
            ]

        # 检查图片数量限制（仅当有图片时）
        if len(valid_files) > self.MAX_TOTAL_IMAGES:
            yield self.create_text_message(
                f"❌ 错误：最多支持 {self.MAX_TOTAL_IMAGES} 张图片，当前提供了 {len(valid_files)} 张"
            )
            return

        # 判断模式：有图片为图生图，无图片为文生图
        is_text_to_image = len(valid_files) == 0
        
        # 获取其他参数
        prompt = str(tool_parameters.get('prompt', ''))
        if not prompt:
            yield self.create_text_message("❌ 错误：必须提供编辑指令")
            return
        
        # Get credentials from runtime (configured in plugin settings)
        api_key = self.runtime.credentials.get('api_key')
        if not api_key:
            yield self.create_text_message("❌ 错误：未配置 API Key，请在插件设置中配置")
            return

        base_url = self.runtime.credentials.get('base_url', 'https://www.16api.com')
        aspect_ratio = tool_parameters.get('aspect_ratio', 'auto')
        image_size = tool_parameters.get('image_size', '2K')
        
        # --- 1. 处理所有输入图片，转换为 base64 ---
        image_parts = []
        image_count = len(valid_files)

        if not is_text_to_image:
            # 图生图模式：处理输入图片
            try:
                yield self.create_text_message(f"⏳ 正在处理 {image_count} 张输入图片...")

                for idx, image_file in enumerate(valid_files):
                    # Get file binary content
                    # Note: In new plugin system, file handling might be different
                    # This assumes File object has blob attribute or similar
                    if hasattr(image_file, 'blob'):
                        img_binary = image_file.blob
                    elif hasattr(image_file, 'read'):
                        img_binary = image_file.read()
                    else:
                        # Fallback: assume image_file is already binary data or has __bytes__
                        img_binary = bytes(image_file)

                    # 转换为 base64
                    img_b64 = base64.b64encode(img_binary).decode('utf-8')

                    # 获取 MIME 类型
                    mime_type = getattr(image_file, 'mime_type', 'image/jpeg') or 'image/jpeg'

                    # 构建 inline_data 部分
                    image_parts.append({
                        "inline_data": {
                            "mime_type": mime_type,
                            "data": img_b64
                        }
                    })

                yield self.create_text_message(f"✅ 成功处理 {image_count} 张图片")

            except Exception as e:
                yield self.create_text_message(f"❌ 处理输入图片失败: {str(e)}")
                return
        else:
            # 文生图模式：无需处理图片
            yield self.create_text_message("📝 文生图模式：将根据文字描述生成图片")
        
        # --- 2. 构建 Gemini API 请求 ---
        # 构建 parts 数组：先放 prompt，再放所有图片
        # 按照 Gemini API 文档格式
        parts = [{"text": prompt}] + image_parts
        
        # 构建 generationConfig
        # 根据 API 文档，responseModalities 必须包含 TEXT 和 IMAGE
        generation_config = {
            "responseModalities": ["TEXT", "IMAGE"]
        }
        
        # 构建 imageConfig
        image_config = {}
        
        # 只有在非 auto 模式下才设置 aspectRatio
        if aspect_ratio and aspect_ratio != "auto":
            image_config["aspectRatio"] = aspect_ratio
        
        # 设置图片质量
        if image_size:
            image_config["imageSize"] = image_size
        
        # 只有在有配置时才加入 imageConfig
        if image_config:
            generation_config["imageConfig"] = image_config
        
        # 最终请求体
        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": parts
                }
            ],
            "generationConfig": generation_config
        }
        
        # --- 3. 调用 Gemini API ---
        try:
            if is_text_to_image:
                yield self.create_text_message("🎨 正在使用 Gemini 根据文字描述生成图片...")
            else:
                yield self.create_text_message(f"🎨 正在使用 Gemini 融合 {image_count} 张图片生成新图...")
            
            # 构建 API URL（根据文档，使用 query parameter 传递 key）
            api_url = f"{base_url}/v1beta/models/gemini-3-pro-image-preview:generateContent"
            
            headers = {
                "Content-Type": "application/json"
            }
            
            params = {
                "key": api_key
            }
            
            # 发起请求（多图片生成较慢，设置较长超时）
            response = requests.post(
                api_url,
                headers=headers,
                params=params,
                json=payload,
                timeout=300  # 5分钟超时（多图需要更长时间）
            )
            
            if response.status_code != 200:
                yield self.create_text_message(
                    f"❌ API 请求失败: HTTP {response.status_code}\n{response.text[:200]}"
                )
                return
            
            result_json = response.json()
            
        except requests.exceptions.Timeout:
            yield self.create_text_message("❌ 请求超时：图片生成时间过长，请稍后重试")
            return
        except requests.exceptions.RequestException as e:
            yield self.create_text_message(f"❌ 网络请求失败: {str(e)}")
            return
        except Exception as e:
            yield self.create_text_message(f"❌ 调用 API 失败: {str(e)}")
            return
        
        # --- 4. 解析响应并提取 base64 图片数据 ---
        try:
            image_b64 = None
            output_mime_type = "image/jpeg"
            text_response = ""
            
            if "candidates" in result_json and len(result_json["candidates"]) > 0:
                candidate = result_json["candidates"][0]
                if "content" in candidate and "parts" in candidate["content"]:
                    parts_list = candidate["content"]["parts"]
                    for part in parts_list:
                        # 提取文本响应
                        if "text" in part:
                            text_response = part["text"]
                        # 提取图片数据 - 支持两种命名格式：inlineData（驼峰）和 inline_data（下划线）
                        inline_data = part.get("inlineData") or part.get("inline_data")
                        if inline_data:
                            image_b64 = inline_data.get("data", "")
                            output_mime_type = inline_data.get("mimeType") or inline_data.get("mime_type", "image/jpeg")
                            if image_b64:
                                break
            
            if not image_b64:
                # 输出更详细的调试信息
                debug_info = f"响应结构: {list(result_json.keys())}"
                if "candidates" in result_json and len(result_json["candidates"]) > 0:
                    candidate = result_json["candidates"][0]
                    if "content" in candidate and "parts" in candidate["content"]:
                        parts_keys = [list(p.keys()) for p in candidate["content"]["parts"]]
                        debug_info += f"\nparts 内容类型: {parts_keys}"
                    if "finishReason" in candidate:
                        debug_info += f"\nfinishReason: {candidate['finishReason']}"
                
                yield self.create_text_message(
                    f"❌ API 未返回图片数据\n{debug_info}\n文本响应: {text_response[:200] if text_response else '无'}"
                )
                return
            
        except Exception as e:
            yield self.create_text_message(f"❌ 解析 API 响应失败: {str(e)}")
            return
        
        # --- 5. 将 base64 转换为图片文件并输出 ---
        try:
            # 解码 base64 为二进制数据
            img_data = base64.b64decode(image_b64)
            
            # 根据 MIME 类型确定文件扩展名
            if "png" in output_mime_type.lower():
                file_extension = ".png"
            else:
                file_extension = ".jpg"
            
            # 生成文件名（根据模式区分）
            if is_text_to_image:
                filename = f"gemini_text2img_{user_id[:6]}{file_extension}"
            else:
                filename = f"gemini_fusion_{image_count}imgs_{user_id[:6]}{file_extension}"

            # 返回图片文件（使用 create_blob_message）
            yield self.create_blob_message(
                blob=img_data,
                meta={
                    'mime_type': output_mime_type,
                    'filename': filename
                }
            )

            if is_text_to_image:
                yield self.create_text_message("✅ 文生图完成！")
            else:
                yield self.create_text_message(f"✅ 图片融合完成！（基于 {image_count} 张输入图片）")
            
        except Exception as e:
            yield self.create_text_message(f"❌ 转换图片文件失败: {str(e)}")
            return
