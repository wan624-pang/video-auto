# video-auto

一个用于自动化处理剪映（CapCut/JianyingPro）草稿的工具：批量导入图片、按字幕时间自动切换图片、为图片添加关键帧与随机入场动画，并生成特效轨道。

注意：仓库中 1.txt/123 - 副本.txt 为来源参考（包含被转义的 Python 代码片段），当前可运行逻辑已重构为 Python 模块。

## 功能
- 自动定位最新草稿（默认搜索 `~/Desktop/Youtube/剪映draft/JianyingPro Drafts/*/draft_content.json`）
- 在指定目录收集图片（默认 `~/Desktop/Youtube/images`）
- 将图片以 `photo` 形式导入到草稿 `materials.videos`
- 依据字幕时间切片图片（保证每张图≥5秒），并为每个片段设置关键帧与随机入场动画
- 追加图片轨道与特效轨道（占位）

## 安装与运行
本项目为纯 Python 项目，无第三方依赖。确保 Python 3.9+。

方式一：模块方式运行

```
python -m video_auto
```

方式二：在代码中调用

```python
from video_auto.sync import process_draft_automatically

# 可传入图片目录，不传则使用默认路径
process_draft_automatically(images_dir="/path/to/images")
```

## 路径与配置
- 草稿路径默认：`~/Desktop/Youtube/剪映draft/JianyingPro Drafts/*/draft_content.json`
- 图片目录默认：`~/Desktop/Youtube/images`
- 最小图片展示时间：5 秒（内部使用微秒进行计算）

如需在不同系统或用户目录上运行，建议在调用时显式传入 `images_dir`，并根据实际情况修改源码中 `get_latest_draft_folder()` 的搜索路径。

## 重要说明
- 为保护草稿安全，实际使用中建议先备份 `draft_content.json` 再运行该工具。
- 不同版本的剪映草稿 JSON 结构可能有所差异，当前实现尽量兼容，如遇不兼容可根据实际结构做适配。

## 目录结构
```
.
├── .gitignore
├── README.md
├── 1.txt/
│   └── 123 - 副本.txt  # 参考文本（被转义的 Python 代码）
└── video_auto/
    ├── __init__.py
    ├── __main__.py     # 入口：python -m video_auto
    └── sync.py         # 核心逻辑
```

## 许可
本仓库未指定 License，如需开源请补充许可证文件。
