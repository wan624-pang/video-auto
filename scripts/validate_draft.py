import json
import os
from typing import Dict, List

MICROSECONDS = 1_000_000


def _track_end_time(track: Dict) -> int:
    end = 0
    for seg in track.get("segments") or []:
        tt = seg.get("target_timerange") or {}
        start = int(tt.get("start") or 0)
        duration = int(tt.get("duration") or 0)
        end = max(end, start + duration)
    return end


def _duration_seconds(us: int) -> float:
    return us / MICROSECONDS


def validate_draft(draft_path: str) -> List[str]:
    errors: List[str] = []
    draft_content = os.path.join(draft_path, "draft_content.json")
    if not os.path.exists(draft_content):
        errors.append("缺少 draft_content.json")
        return errors

    with open(draft_content, "r", encoding="utf-8") as f:
        draft = json.load(f)

    tracks = draft.get("tracks") or []
    if len(tracks) < 2:
        errors.append("轨道数量过少，期望至少包含视频与音频/文本")

    # 估算视频轨与音频/文本轨的时长一致性
    video_like = [t for t in tracks if str(t.get("type")).lower() in {"video", "sticker"}]
    audio_like = [t for t in tracks if str(t.get("type")).lower() in {"audio", "text", "subtitle"}]

    if video_like:
        video_end = max(_track_end_time(t) for t in video_like)
    else:
        video_end = 0

    if audio_like:
        audio_end = max(_track_end_time(t) for t in audio_like)
    else:
        audio_end = 0

    if video_end and audio_end:
        if abs(_duration_seconds(video_end - audio_end)) > 0.5:
            errors.append("音画时长差异超过 0.5 秒，请检查时间线对齐")

    return errors


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Validate CapCut draft")
    parser.add_argument("path", help="draft 文件夹路径")
    args = parser.parse_args()

    errs = validate_draft(args.path)
    if errs:
        print("验证失败：")
        for e in errs:
            print("- ", e)
    else:
        print("验证通过")
