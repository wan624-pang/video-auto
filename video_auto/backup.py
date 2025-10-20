import os
import shutil
from datetime import datetime


def backup_draft(src: str, dest_dir: str) -> str:
    src = os.path.abspath(src)
    os.makedirs(dest_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base = os.path.join(dest_dir, f"backup_{timestamp}")
    archive_path = shutil.make_archive(base, "zip", src)
    return archive_path
