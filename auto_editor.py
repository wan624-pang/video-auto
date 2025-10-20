import argparse
from editor import render_video


def main() -> None:
    parser = argparse.ArgumentParser(description="Video Auto Editor CLI")
    parser.add_argument("--manifest", required=True, help="manifest.json 路径")
    parser.add_argument("--preset", default=None, help="预设名称，可选")
    parser.add_argument("--output", default=None, help="输出目录，可选")
    args = parser.parse_args()

    folder = render_video(args.manifest, preset_name=args.preset, output_dir=args.output)
    print(f"已更新草稿: {folder}")


if __name__ == "__main__":
    main()
