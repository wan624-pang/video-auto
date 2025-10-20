import os
import json
from typing import Any, Dict, List, Optional


class Manifest:
    def __init__(self, data: Dict[str, Any], base_dir: str) -> None:
        self.data = data
        self.base_dir = base_dir

    def resolve_path(self, path: Optional[str]) -> Optional[str]:
        if not path:
            return None
        if os.path.isabs(path):
            return path
        return os.path.join(self.base_dir, path)

    def get_project_name(self) -> str:
        return str(self.data.get("project_name") or self.data.get("project", {}).get("name") or "untitled")

    def get_assets(self) -> Dict[str, List[str]]:
        assets: Dict[str, Any] = self.data.get("assets", {}) or {}
        images = [self.resolve_path(p) for p in assets.get("images", [])]
        audio = [self.resolve_path(p) for p in assets.get("audio", [])]
        fonts = [self.resolve_path(p) for p in assets.get("fonts", [])]
        bgm = assets.get("bgm")
        bgm_path = self.resolve_path(bgm) if isinstance(bgm, str) else None
        return {
            "images": [p for p in images if p],
            "audio": [p for p in audio if p],
            "fonts": [p for p in fonts if p],
            "bgm": [bgm_path] if bgm_path else [],
        }

    def get_draft_settings(self) -> Dict[str, Any]:
        ds = self.data.get("draft_settings", {}) or {}
        draft_path = self.resolve_path(ds.get("draft_path")) if ds.get("draft_path") else None
        backup_conf = ds.get("backup", {}) or {}
        backup_enable = bool(backup_conf.get("enable", False))
        backup_location = self.resolve_path(backup_conf.get("location")) if backup_conf.get("location") else None
        return {
            "draft_path": draft_path,
            "backup": {
                "enable": backup_enable,
                "location": backup_location,
            },
        }


def load_manifest(manifest_path: str) -> Manifest:
    manifest_path = os.path.abspath(manifest_path)
    with open(manifest_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    base_dir = os.path.dirname(manifest_path)
    return Manifest(data, base_dir)


def validate_manifest_basic(data: Dict[str, Any]) -> List[str]:
    errors: List[str] = []
    if not isinstance(data, dict):
        return ["manifest 必须是 JSON 对象"]
    if "project_name" not in data and "project" not in data:
        errors.append("缺少 project_name（或旧版 project.name）")
    if "assets" not in data or not isinstance(data.get("assets"), dict):
        errors.append("缺少 assets 对象")
    else:
        assets = data["assets"]
        if "images" not in assets and "audio" not in assets and "bgm" not in assets:
            errors.append("assets 至少包含 images/audio/bgm 之一")
        for key in ("images", "audio", "fonts"):
            if key in assets and not isinstance(assets[key], list):
                errors.append(f"assets.{key} 必须是数组")
    return errors
