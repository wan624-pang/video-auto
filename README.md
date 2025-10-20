# video-auto

一个用于自动化处理剪映（CapCut/JianyingPro）草稿的工具：批量导入图片、按字幕时间自动切换图片、为图片添加关键帧与随机入场动画，并生成特效轨道。

注意：仓库中 1.txt/123 - 副本.txt 为来源参考（包含被转义的 Python 代码片段），当前可运行逻辑已重构为 Python 模块。

## 功能
- 自动定位最新草稿（默认搜索 `~/Desktop/Youtube/剪映draft/JianyingPro Drafts/*/draft_content.json`）
- 在指定目录收集图片（默认 `~/Desktop/Youtube/images`）
- 将图片以 `photo` 形式导入到草稿 `materials.videos`
- 依据字幕时间切片图片（保证每张图≥5秒），并为每个片段设置关键帧与随机入场动画
- 追加图片轨道与特效轨道（占位）
- 新增：基于 manifest（资产清单）加载图片并更新草稿；提供 CLI 与 API（render_video）

## 安装与运行
本项目为纯 Python 项目，无第三方依赖。确保 Python 3.9+。

方式一：模块方式运行

```
python -m video_auto
```

方式二：在代码中调用（旧接口）

```python
from video_auto.sync import process_draft_automatically

# 可传入图片目录，不传则使用默认路径
process_draft_automatically(images_dir="/path/to/images")
```

方式三：CLI（新）

```
python auto_editor.py --manifest path/to/manifest.json --preset 横屏
```

方式四：API（新）

```python
from editor import render_video

render_video(
    manifest_path="path/to/manifest.json",
    preset_name="竖屏",
    output_dir="/path/to/output"
)
```

## 路径与配置
- 草稿路径默认：`~/Desktop/Youtube/剪映draft/JianyingPro Drafts/*/draft_content.json`（Linux 默认）；Windows 与 macOS 会使用各自默认草稿根目录自动搜寻。
- 资产清单 manifest（v2：assets 版）示例：`examples/manifest.assets.example.json`
- JSON Schema：`docs/manifest.assets.schema.json`
- 旧版（timeline）Schema：`docs/manifest.schema.json`

如需在不同系统或用户目录上运行，建议在调用时显式传入 manifest 中的 `draft_settings.draft_path`，或根据实际情况修改源码中的默认路径。

## 重要说明
- 为保护草稿安全，实际使用中建议开启 manifest 中的备份选项，或手动备份 `draft_content.json` 再运行。
- 不同版本的剪映草稿 JSON 结构可能有所差异，当前实现尽量兼容，如遇不兼容可根据实际结构做适配。

## 目录结构
```
.
├── .gitignore
├── README.md
├── 1.txt/
│   └── 123 - 副本.txt  # 参考文本（被转义的 Python 代码）
├── docs/
│   ├── plan.md                        # 方案与执行清单
│   ├── manifest.schema.json           # 旧版（timeline）Schema 草案
│   └── manifest.assets.schema.json    # 新版（assets）Schema
├── examples/
│   ├── manifest.example.json          # 旧版示例
│   └── manifest.assets.example.json   # 新版示例
├── scripts/
│   └── validate_draft.py              # 草稿验证脚本（结构/时长粗检）
└── video_auto/
    ├── __init__.py
    ├── __main__.py                    # 入口：python -m video_auto
    ├── api.py                         # 新：对外 API（render_video）
    ├── backup.py                      # 备份工具
    ├── config.py                      # manifest 加载/路径解析
    ├── paths.py                       # 跨平台草稿路径发现
    ├── presets.py                     # 预设占位
    └── sync.py                        # 核心逻辑
```

## 许可
本仓库未指定 License，如需开源请补充许可证文件。
