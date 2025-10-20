import os
import platform
from glob import glob
from typing import Optional


def get_default_draft_root() -> str:
    system = platform.system().lower()
    if system.startswith("windows"):
        return os.path.expanduser("~/AppData/Local/JianyingPro/User Data/Projects/com.lveditor.draft")
    elif system == "darwin":
        return os.path.expanduser("~/Movies/JianyingPro/User Data/Projects/com.lveditor.draft")
    else:
        return os.path.expanduser("~/Desktop/Youtube/剪映draft/JianyingPro Drafts")


def find_draft_content_json(draft_path: Optional[str]) -> Optional[str]:
    if draft_path:
        draft_path = os.path.abspath(draft_path)
        if os.path.isdir(draft_path):
            candidate = os.path.join(draft_path, "draft_content.json")
            if os.path.exists(candidate):
                return candidate
            matches = glob(os.path.join(draft_path, "**", "draft_content.json"), recursive=True)
            if matches:
                matches.sort(key=os.path.getmtime, reverse=True)
                return matches[0]
        elif os.path.isfile(draft_path) and draft_path.endswith("draft_content.json"):
            return draft_path
    root = get_default_draft_root()
    matches = glob(os.path.join(root, "**", "draft_content.json"), recursive=True)
    if not matches:
        return None
    matches.sort(key=os.path.getmtime, reverse=True)
    return matches[0]
