import os
import json
import uuid
import random
from glob import glob
from datetime import datetime
from typing import Any, Dict, List, Optional

# 最小图片展示时间（秒）
MIN_IMAGE_DURATION_SECONDS = 5
MICROSECONDS = 1_000_000


def microsec_to_time(microseconds: int) -> str:
    """将微秒转换为 MM:SS:MS 字符串"""
    total_seconds = microseconds / MICROSECONDS
    minutes = int(total_seconds // 60)
    seconds = int(total_seconds % 60)
    ms = int((total_seconds % 1) * 1000)
    return f"{minutes:02d}:{seconds:02d}:{ms:03d}"


def format_duration(microseconds: int) -> str:
    return f"{microseconds / MICROSECONDS:.2f}秒"


def get_latest_draft_folder() -> str:
    """获取最新的剪映草稿文件夹。

    默认搜索路径（可根据实际系统调整）:
    ~/Desktop/Youtube/剪映draft/JianyingPro Drafts/*/draft_content.json
    """
    draft_pattern = os.path.expanduser(
        "~/Desktop/Youtube/剪映draft/JianyingPro Drafts/*/draft_content.json"
    )
    draft_files = glob(draft_pattern)
    if not draft_files:
        raise FileNotFoundError("未找到剪映草稿文件。请检查草稿存放路径。")
    latest_draft_file = max(draft_files, key=os.path.getmtime)
    return os.path.dirname(latest_draft_file)


def find_images_in_folder(folder_path: Optional[str] = None) -> List[str]:
    """在指定文件夹中查找图片文件，若未提供则搜索默认目录与当前目录。

    支持扩展名：jpg、jpeg、png、gif、webp
    """
    if folder_path is None:
        folder_path = os.path.expanduser("~/Desktop/Youtube/images")

    image_extensions = ["jpg", "jpeg", "png", "gif", "webp"]

    image_files: List[str] = []
    for ext in image_extensions:
        pattern = os.path.join(folder_path, f"*.{ext}")
        image_files.extend(glob(pattern))

    if not image_files:
        current_folder = os.path.dirname(os.path.abspath(__file__))
        for ext in image_extensions:
            pattern = os.path.join(current_folder, f"*.{ext}")
            image_files.extend(glob(pattern))

    return image_files


def ensure_materials(draft: Dict[str, Any]) -> None:
    if "materials" not in draft:
        draft["materials"] = {}
    if "videos" not in draft["materials"]:
        draft["materials"]["videos"] = []
    if "material_animations" not in draft["materials"]:
        draft["materials"]["material_animations"] = []


def import_images_to_draft(draft: Dict[str, Any], image_files: List[str]) -> List[Dict[str, Any]]:
    """将图片作为 photo 类型素材导入到 materials.videos 中，返回导入的素材列表。"""
    ensure_materials(draft)

    image_materials: List[Dict[str, Any]] = []
    for image_file in image_files:
        image_id = str(uuid.uuid4())
        file_name = os.path.basename(image_file)

        image_material = {
            "aigc_type": "none",
            "audio_fade": None,
            "cartoon_path": "",
            "category_id": "",
            "category_name": "",
            "check_flag": 0,
            "crop": {
                "lower_left_x": 0.0,
                "lower_left_y": 1.0,
                "lower_right_x": 1.0,
                "lower_right_y": 1.0,
                "upper_left_x": 0.0,
                "upper_left_y": 0.0,
                "upper_right_x": 1.0,
                "upper_right_y": 0.0,
            },
            "crop_ratio": "free",
            "crop_scale": 1.0,
            "duration": 0,
            "formula_id": "",
            "freeze": None,
            "has_audio": False,
            "height": 1080,
            "id": image_id,
            "intensifies_audio_path": "",
            "intensifies_path": "",
            "is_ai_generate_content": False,
            "is_copyright": False,
            "is_text_edit_overdub": False,
            "is_unified_beauty_mode": False,
            "local_id": "",
            "local_material_id": "",
            "material_id": "",
            "material_name": file_name,
            "material_url": "",
            "matting": {
                "flag": 0,
                "has_use_quick_brush": False,
                "has_use_quick_eraser": False,
                "interactiveTime": [],
                "path": "",
                "strokes": [],
            },
            "media_path": "",
            "object_locked": None,
            "origin_material_id": "",
            "path": image_file,
            "picture_from": "none",
            "picture_set_category_id": "",
            "picture_set_category_name": "",
            "request_id": "",
            "reverse_intensifies_path": "",
            "reverse_path": "",
            "smart_motion": None,
            "source": 0,
            "source_platform": 0,
            "stable": {
                "matrix_path": "",
                "stable_level": 0,
                "time_range": {"duration": 0, "start": 0},
            },
            "team_id": "",
            "type": "photo",
            "video_algorithm": {
                "algorithms": [],
                "complement_frame_config": None,
                "deflicker": None,
                "gameplay_configs": [],
                "motion_blur_config": None,
                "noise_reduction": None,
                "path": "",
                "quality_enhance": None,
                "time_range": None,
            },
            "width": 1920,
        }
        draft["materials"]["videos"].append(image_material)
        image_materials.append(image_material)

    return image_materials


def _kf(property_type: str, values_start: float, values_end: float, duration: int) -> Dict[str, Any]:
    return {
        "id": str(uuid.uuid4()),
        "keyframe_list": [
            {"time_offset": 0, "values": [values_start]},
            {"time_offset": duration, "values": [values_end]},
        ],
        "property_type": property_type,
    }


def create_common_keyframes(start_time: int, duration: int, movement_type: Optional[str] = None) -> List[Dict[str, Any]]:
    """创建简单的平移关键帧（X/Y），用于营造缓慢移动效果。"""
    if movement_type is None:
        movement_type = random.choice(["left", "right", "up", "down"])

    if movement_type in ["left", "right"]:
        x_start = -0.21 if movement_type == "left" else 0.21
        x_end = -x_start
        return [
            _kf("KFTypePositionX", x_start, x_end, duration),
            _kf("KFTypePositionY", 0, 0, duration),
        ]
    else:
        y_start = -0.21 if movement_type == "up" else 0.21
        y_end = -y_start
        return [
            _kf("KFTypePositionX", 0, 0, duration),
            _kf("KFTypePositionY", y_start, y_end, duration),
        ]


def _anim(name: str, resource_id: str) -> Dict[str, Any]:
    """创建一个简化的动画描述对象。"""
    animation_id = str(uuid.uuid4())
    request_id = datetime.now().strftime("%Y%m%d%H%M%S") + str(uuid.uuid4())[:8].upper()
    return {
        "animations": [
            {
                "anim_adjust_params": None,
                "category_id": "in",
                "category_name": "入场",
                "duration": 700_000,
                "id": resource_id,
                "material_type": "video",
                "name": name,
                "panel": "video",
                "path": "",
                "platform": "all",
                "request_id": request_id,
                "resource_id": resource_id,
                "start": 0,
                "type": "in",
            }
        ],
        "id": animation_id,
        "type": "sticker_animation",
    }


def create_fade_animation() -> Dict[str, Any]:
    return _anim("渐显", "fade")


def create_scale_animation() -> Dict[str, Any]:
    return _anim("向右甩入", "scale_in_right")


def create_bounce_animation() -> Dict[str, Any]:
    return _anim("向左滑动", "slide_in_left")


def create_wiper_animation() -> Dict[str, Any]:
    return _anim("雨刷 II", "wiper")


def create_shake_animation() -> Dict[str, Any]:
    return _anim("左右抖动", "shake")


def get_random_animation() -> Dict[str, Any]:
    return random.choice(
        [
            create_fade_animation(),
            create_scale_animation(),
            create_bounce_animation(),
            create_wiper_animation(),
            create_shake_animation(),
        ]
    )


def get_segment_start(seg: Dict[str, Any]) -> Optional[int]:
    # 兼容不同草稿结构：优先使用 target_timerange.start
    tt = seg.get("target_timerange") or {}
    if isinstance(tt, dict) and "start" in tt:
        return int(tt.get("start") or 0)
    # 兜底：source_timerange.start
    st = seg.get("source_timerange") or {}
    if isinstance(st, dict) and "start" in st:
        return int(st.get("start") or 0)
    return None


def get_subtitle_segments_from_draft(draft: Dict[str, Any]) -> List[Dict[str, Any]]:
    """从草稿中提取字幕片段列表。不同版本结构可能不同，这里尽量兼容。"""
    tracks = draft.get("tracks") or []
    subtitle_segments: List[Dict[str, Any]] = []
    for track in tracks:
        ttype = track.get("type") or track.get("track_type") or ""
        if str(ttype).lower() in {"text", "subtitle", "sticker"}:  # 字幕/文本可能标记不同
            for seg in track.get("segments") or []:
                # 若包含文本/字幕属性，认为是字幕片段
                attrs = seg.get("attrs") or {}
                if any(k in seg for k in ("text", "subtitle")) or attrs.get("is_text"):
                    subtitle_segments.append(seg)
    # 按开始时间排序
    subtitle_segments.sort(key=lambda s: get_segment_start(s) or 0)
    return subtitle_segments


def find_next_subtitle_time(subtitle_segments: List[Dict[str, Any]], start_time: int) -> int:
    min_end = start_time + MIN_IMAGE_DURATION_SECONDS * MICROSECONDS
    candidates: List[int] = []
    for seg in subtitle_segments:
        st = get_segment_start(seg)
        if st is None:
            continue
        if st >= min_end:
            candidates.append(st)
    if candidates:
        return min(candidates)
    # 若没有更远的字幕，则按最短时长结束
    return min_end


def build_image_segment(material_id: str, start_time: int, duration: int, render_index: int) -> Dict[str, Any]:
    seg = {
        "cartoon": False,
        "clip": {
            "alpha": 1.0,
            "flip": {"horizontal": False, "vertical": False},
            "rotation": 0.0,
            "scale": {"x": 1.25, "y": 1.25},
            "transform": {"x": 0.0, "y": 0.0},
        },
        "common_keyframes": [],
        "enable_adjust": False,
        "enable_color_curves": True,
        "enable_color_wheels": True,
        "extra_material_refs": [],
        "group_id": "",
        "id": str(uuid.uuid4()),
        "intensifies_audio": False,
        "is_placeholder": False,
        "material_id": material_id,
        "render_index": render_index,
        "source_timerange": {"duration": duration, "start": 0},
        "speed": 1.0,
        "target_timerange": {"duration": duration, "start": start_time},
        "template_id": "",
        "template_scene": "default",
        "track_attribute": 0,
        "track_render_index": 0,
        "uniform_scale": {"on": True, "value": 1.0},
        "visible": True,
        "volume": 1.0,
    }
    return seg


def add_effect_track(draft: Dict[str, Any], created_segments: List[Dict[str, Any]]) -> Dict[str, Any]:
    """创建一个简单的特效轨道（占位），方便后续在剪映中微调。"""
    effect_track = {
        "attribute": 0,
        "flag": 0,
        "id": str(uuid.uuid4()),
        "segments": [],
        "type": "effect",
    }
    # 可按需基于 created_segments 创建对应的特效片段，这里留空占位
    return effect_track


def ensure_tracks(draft: Dict[str, Any]) -> None:
    if "tracks" not in draft or not isinstance(draft["tracks"], list):
        draft["tracks"] = []


def sync_images_with_subtitles_in_draft(draft: Dict[str, Any], images_dir: Optional[str] = None) -> Dict[str, Any]:
    """按照字幕时间创建图片片段，设置关键帧与随机动画，并生成特效轨道。"""
    ensure_materials(draft)
    ensure_tracks(draft)

    subtitle_segments = get_subtitle_segments_from_draft(draft)
    image_files = find_images_in_folder(images_dir)

    image_materials = import_images_to_draft(draft, image_files)

    # 若没有图片，创建一个默认占位素材
    if not image_materials:
        default_image = {
            "id": str(uuid.uuid4()),
            "type": "photo",
            "path": "",
            "material_name": "placeholder",
            "width": 1920,
            "height": 1080,
        }
        draft["materials"]["videos"].append(default_image)
        image_materials = [default_image]

    # 创建图片轨道
    image_track = {
        "attribute": 0,
        "flag": 0,
        "id": str(uuid.uuid4()),
        "segments": [],
        "type": "video",
    }

    last_end_time = 0
    created_segments: List[Dict[str, Any]] = []

    if not subtitle_segments:
        # 无字幕时，至少铺 1 段 5 秒
        duration = MIN_IMAGE_DURATION_SECONDS * MICROSECONDS
        mat = image_materials[0]
        seg = build_image_segment(mat["id"], last_end_time, duration, 0)
        seg["common_keyframes"] = create_common_keyframes(last_end_time, duration)
        anim = get_random_animation()
        draft["materials"]["material_animations"].append(anim)
        seg["extra_material_refs"].append(anim["id"])
        image_track["segments"].append(seg)
        created_segments.append(seg)
    else:
        for i in range(len(subtitle_segments)):
            start_time = last_end_time
            end_time = find_next_subtitle_time(subtitle_segments, start_time)
            duration = end_time - start_time

            mat = image_materials[i % len(image_materials)]
            seg = build_image_segment(mat["id"], start_time, duration, i)

            # 关键帧与动画
            seg["common_keyframes"] = create_common_keyframes(start_time, duration)
            anim = get_random_animation()
            draft["materials"]["material_animations"].append(anim)
            seg["extra_material_refs"].append(anim["id"])

            image_track["segments"].append(seg)
            created_segments.append(seg)

            last_end_time = end_time

    # 追加特效轨道
    effect_track = add_effect_track(draft, created_segments)
    draft["tracks"].append(image_track)
    draft["tracks"].append(effect_track)
    return draft


def process_draft_automatically(images_dir: Optional[str] = None) -> None:
    """自动处理最新的剪映草稿：导入图片，按字幕切片，添加关键帧与动画。"""
    latest_draft_folder = get_latest_draft_folder()
    draft_content_path = os.path.join(latest_draft_folder, "draft_content.json")

    # 读取草稿
    with open(draft_content_path, "r", encoding="utf-8") as f:
        draft = json.load(f)

    # 同步
    draft = sync_images_with_subtitles_in_draft(draft, images_dir)

    # 写回（建议实际环境中先做备份）
    with open(draft_content_path, "w", encoding="utf-8") as f:
        json.dump(draft, f, ensure_ascii=False)

    print(f"成功将图片与字幕同步到草稿: {latest_draft_folder}")
