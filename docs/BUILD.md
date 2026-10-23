# 构建与复现

Python 3.12。安装 `requirements.txt` 中锁定的 Pillow、NumPy 与 SciPy，然后运行：

```sh
python scripts/build.py
python scripts/validate.py
python scripts/render_previews.py
python scripts/release.py
```

`build.py` 调用 `choreography.py`，从 `sources/frames/` 的透明切帧、裁剪位置与相对坐标生成三套图集：

1. 清理每张切帧的边缘：去掉半透明暗色污边；清晰版休息姿态的紫边改为深色描边（动漫版的紫色描边是设计本身，保留）。
2. 在 3 倍单元格分辨率下按行编排：整体位移、倾斜、挤压拉伸、碎发独立漂移、running-left 逐帧镜像、
   在原眼睛位置画闭眼线；最后一次性缩小到 192×208。清晰版用 Q 版切帧，动漫版用动漫切帧，两套姿势顺序相同。
3. 像素版把清晰版成品缩到 48×52 逻辑像素，按 `sources/pixel/palette.json` 的 32 色量化，再最近邻放大 4 倍。

时序常量 `HOST_DURATIONS` 与 Codex / Petdex 默认值一致；改动作时先改这里，再更新包内
`animation-manifest.json` 与 `catalogue.json`。确认要替换批准稿时运行 `python scripts/build.py --approve`，
它会写入 `pets/*/spritesheet.*` 并更新像素指纹，之后运行 `update_preview.py` 和 `render_previews.py`。
`render_previews.py` 从实际打包的图集生成 README 用的 GIF、状态总览图，以及 ⑤⑥ 的画廊卡片。
图集在 Pillow 12.3 / NumPy 2.2 与锁定版本下得到相同像素指纹。
`sources/pixel/atlas-1x.png` 是 v1.0 像素版的逻辑图集，作为制作阶段存档保留，构建不再使用。
结果写入 `dist/rebuilt/pets/`，不会覆盖仓库附带的批准稿或本机已安装宠物。
校验同时检查图集几何、PNG/WebP逐像素一致、使用帧非空、未使用帧透明，以及目录穿越和版本ID。
重建结果需要和 `catalogue.json` 记录的批准稿 RGBA 像素指纹相符。

高清图生成和切帧发生在此前制作阶段；本仓库保留结果、提示词及透明帧。
不声称能确定性重现 AI 生成过程。v1.0 像素化曾使用外部工具做32色量化；这里保留当时的调色板，
现在的像素版用同一调色板在本仓库内量化，不需要安装作者本机的 skill。
不同 Pillow 版本的重采样或压缩可能不同；像素校验失败时应先检查依赖版本，不能静默替换批准稿。

`release.py` 先做本地包校验，再导出三个角色 ZIP、原稿归档 ZIP 和完整源码 ZIP，写入 SHA256SUMS.txt。
完整源码包包含工具与原稿，不包含 `.git`、`dist`、缓存或系统配置。
`.github/workflow-templates/` 提供提交校验与标签发行的 CI 模板，默认不启用自动发布。
维护者希望启用时，将模板复制到 `.github/workflows/` 后提交；按 GitHub 要求授予工作流权限。
标签发行模板会校验标签与 `catalogue.json` 版本一致，再创建包含校验和的 Release。
