import json
import os
from typing import List, Optional

from .config import load_manifest
from .paths import find_draft_content_json
from .backup import backup_draft
from . import sync


def _compute_end_time(segments: List[dict]) -> int:
    end = 0
    for seg in segments or []:
        tt = seg.get("target_timerange") or {}
        start = int(tt.get("start") or 0)
        duration = int(tt.get("duration") or 0)
        end = max(end, start + duration)
    return end


def _ensure_effect_track(draft: dict) -> None:
    if "tracks" not in draft:
        draft["tracks"] = []
    # 避免重复添加，占位一次
    if not any(t.get("type") == "effect" for t in draft["tracks"]):
        effect_track = sync.add_effect_track(draft, [])
        draft["tracks"].append(effect_track)


def render_video(manifest_path: str, preset_name: Optional[str] = None, output_dir: Optional[str] = None) -> str:
    mf = load_manifest(manifest_path)
    ds = mf.get_draft_settings()

    draft_content = find_draft_content_json(ds.get("draft_path"))
    if not draft_content:
        raise FileNotFoundError("未找到 draft_content.json，请检查 draft_path 或默认草稿目录")

    draft_folder = os.path.dirname(draft_content)

    if ds.get("backup", {}).get("enable") and ds.get("backup", {}).get("location"):
        backup_draft(draft_folder, ds["backup"]["location"])

    with open(draft_content, "r", encoding="utf-8") as f:
        draft = json.load(f)

    assets = mf.get_assets()
    image_files: List[str] = assets.get("images", [])

    sync.ensure_materials(draft)
    sync.ensure_tracks(draft)

    if image_files:
        image_materials = sync.import_images_to_draft(draft, image_files)
        subtitle_segments = sync.get_subtitle_segments_from_draft(draft)

        image_track = {
            "attribute": 0,
            "flag": 0,
            "id": os.urandom(8).hex(),
            "segments": [],
            "type": "video",
        }

        created_segments: List[dict] = []
        last_end_time = 0

        if not subtitle_segments:
            duration = sync.MIN_IMAGE_DURATION_SECONDS * sync.MICROSECONDS
            mat = image_materials[0]
            seg = sync.build_image_segment(mat["id"], last_end_time, duration, 0)
            seg["common_keyframes"] = sync.create_common_keyframes(last_end_time, duration)
            anim = sync.get_random_animation()
            draft["materials"]["material_animations"].append(anim)
            seg["extra_material_refs"].append(anim["id"])
            image_track["segments"].append(seg)
            created_segments.append(seg)
        else:
            for i, _ in enumerate(subtitle_segments):
                start_time = last_end_time
                end_time = sync.find_next_subtitle_time(subtitle_segments, start_time)
                duration = end_time - start_time
                mat = image_materials[i % len(image_materials)]
                seg = sync.build_image_segment(mat["id"], start_time, duration, i)
                seg["common_keyframes"] = sync.create_common_keyframes(start_time, duration)
                anim = sync.get_random_animation()
                draft["materials"]["material_animations"].append(anim)
                seg["extra_material_refs"].append(anim["id"])
                image_track["segments"].append(seg)
                created_segments.append(seg)
                last_end_time = end_time

        draft["tracks"].append(image_track)
        _ensure_effect_track(draft)

    with open(draft_content, "w", encoding="utf-8") as f:
        json.dump(draft, f, ensure_ascii=False)

    return draft_folder
