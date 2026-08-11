import base64
import io
import time
from pathlib import Path

import requests
from PIL import Image, ImageOps

from config import get_settings, STYLE_PROMPTS, normalize_size


class VStudioAgent:
    def __init__(self):
        self.settings = get_settings()
        self.output_dir = Path(self.settings["output_dir"])
        if not self.output_dir.is_absolute():
            self.output_dir = Path(__file__).resolve().parent / self.output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.session = requests.Session()

    def _get_api_key(self):
        api_key = self.settings["ark_api_key"]
        if not api_key:
            raise RuntimeError("未检测到 ARK_API_KEY")
        if api_key.lower().startswith("bearer "):
            api_key = api_key[7:].strip()
        return api_key

    def _build_prompt(self, prompt: str, style: str, has_image: bool):
        prompt = (prompt or "").strip()
        style_prompt = STYLE_PROMPTS.get(style, "")

        if not prompt and has_image:
            prompt = "请基于参考图生成高质量结果，保持主体一致，提升画面完成度。"

        if not prompt and not has_image:
            raise RuntimeError("请输入文本内容，或上传参考图片。")

        if style_prompt:
            return f"{style_prompt}\n\n{prompt}".strip()

        return prompt

    def _to_data_url(self, image: Image.Image):
        image = ImageOps.exif_transpose(image).convert("RGB")
        max_side = 2048

        if max(image.size) > max_side:
            image.thumbnail((max_side, max_side), Image.Resampling.LANCZOS)

        buffer = io.BytesIO()
        image.save(buffer, format="JPEG", quality=92, optimize=True)
        encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")
        return f"data:image/jpeg;base64,{encoded}"

    def _parse_response_image(self, payload: dict):
        data = payload.get("data") or []
        if not data:
            raise RuntimeError(f"接口返回为空：{payload}")

        item = data[0]

        if item.get("url"):
            response = self.session.get(
                item["url"],
                timeout=(20, self.settings["request_timeout"])
            )
            response.raise_for_status()
            return Image.open(io.BytesIO(response.content)).convert("RGB")

        if item.get("b64_json"):
            raw = base64.b64decode(item["b64_json"])
            return Image.open(io.BytesIO(raw)).convert("RGB")

        raise RuntimeError(f"无法解析返回内容：{item}")

    def _save_output(self, image: Image.Image):
        ts = time.strftime("%Y%m%d_%H%M%S")
        output_path = self.output_dir / f"vstudio_{ts}.png"
        image.save(output_path)
        return str(output_path)

    def generate(self, prompt: str, reference_image: Image.Image, style: str, size: str, temperature: float):
        final_prompt = self._build_prompt(prompt, style, reference_image is not None)
        api_size = normalize_size(size)

        headers = {
            "Authorization": f"Bearer {self._get_api_key()}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.settings["ark_model"],
            "prompt": final_prompt,
            "size": api_size,
            "response_format": "url",
            "watermark": False,
            "temperature": temperature
        }

        if reference_image is not None:
            payload["image"] = self._to_data_url(reference_image)

        try:
            response = self.session.post(
                self.settings["ark_base_url"],
                headers=headers,
                json=payload,
                timeout=(20, self.settings["request_timeout"])
            )
        except requests.RequestException as exc:
            raise RuntimeError(f"请求失败：{exc}") from exc

        if not response.ok:
            try:
                detail = response.json()
            except Exception:
                detail = response.text
            raise RuntimeError(f"Seedream API 请求失败：\nHTTP {response.status_code}\n{detail}")

        try:
            result = response.json()
        except ValueError as exc:
            raise RuntimeError("接口返回不是合法 JSON") from exc

        output_image = self._parse_response_image(result)
        output_path = self._save_output(output_image)

        return output_image, output_path