<div align="center">

# 摩羯 · Capri Desktop Pet

**一只粉红色的小伙伴，六个制作阶段，三套可用桌宠包。**

[English](README.en.md) · **[下载最新版](https://github.com/X1a0heZzzz/capri-desktop-pet/releases/latest)** · [版本画廊](#六个制作阶段) · [安装说明](docs/INSTALL.md) · [离线预览源码](index.html) · [角色素材说明](ASSET_RIGHTS.md)

![清晰版动作预览](docs/previews/capri-clear.gif)

</div>

保留摩羯从初稿、休息姿态、动漫细化到 Q 版原稿、像素化和清晰桌宠的全部现存制作阶段。
默认推荐 **Q版清晰原稿**：保留头发纹理、白色/绿色眼框、嘴形，以及坐下、托腮、侧躺和打盹姿态。

这是**角色包与制作工具仓库**。桌面悬浮、拖动、置顶和任务状态由 Petdex / 兼容宿主提供。

## 直接开始

1. 从仓库下载 ZIP 并解压，或从 Releases 下载单个角色包。
2. 看清晰版：双击仓库根目录 `index.html`；网页完全离线，支持三套包、九种状态切换、暂停和速度调整。
3. 导入桌宠：选择 `pets/capri-clear/`，按 [安装说明](docs/INSTALL.md) 操作。
4. 想要复现导出：见 [构建说明](docs/BUILD.md)。无需模型密钥，也不会联网生成新图。

## 六个制作阶段

| 阶段 | 展示 | 原稿 / 可用包 |
| --- | --- | --- |
| ① 最初角色稿 | [查看](docs/gallery/01-initial.jpg) | [原始 PNG](sources/artwork/01-initial/character.png)，造型研究 |
| ② 休息姿态初稿 | [查看](docs/gallery/02-rest-draft.jpg) | [原始 PNG](sources/artwork/02-rest-draft/rest-poses.png)，姿态研究 |
| ③ 动漫细化版 | [查看](docs/gallery/03-anime-refined.jpg) | [原稿](sources/artwork/03-anime-refined/) · [桌宠包](pets/capri-anime/) |
| ④ Q版清晰原稿 | [查看](docs/gallery/04-chibi-originals.jpg) | [表情与休息原稿](sources/artwork/04-chibi-originals/)，⑥ 的来源 |
| ⑤ Q版像素桌宠 | [查看](docs/gallery/05-pixel-petdex.jpg) | [桌宠包](pets/capri-pixel/)，48×52 逻辑单帧、4倍放大 |
| ⑥ Q版清晰桌宠 ★ | [查看](docs/gallery/06-clear-codex.jpg) | [推荐桌宠包](pets/capri-clear/)，192×208 单帧 |

<details><summary>展开全部版本</summary>

![① 初稿](docs/gallery/01-initial.jpg)
![② 休息初稿](docs/gallery/02-rest-draft.jpg)
![③ 动漫细化](docs/gallery/03-anime-refined.jpg)
![④ Q版原稿](docs/gallery/04-chibi-originals.jpg)
![⑤ 像素版](docs/gallery/05-pixel-petdex.jpg)
![⑥ 清晰版](docs/gallery/06-clear-codex.jpg)

</details>

六个阶段不等于六套独立可运行角色包。①②④保留设计稿；③⑤⑥附完整图集。
旧的 `Capri-Codex` 和后来的「Q版清晰原稿」使用相同图集，只改了名称与描述，合并为⑥，见 [版本记录](CHANGELOG.md)。

## 动作与兼容性

三套图集均为 **1536×1872 / 8列×9行 / 192×208 每帧**，带透明 PNG 和无损 WebP。

| 行 | 状态 | 内容 |
| --- | --- | --- |
| 0 | idle | 发呆、坐下、休息 |
| 1 / 2 | running-right / running-left | 左右移动时的关键姿态 |
| 3 | waving | 招呼与表情变化 |
| 4 | jumping | 小幅跳动 |
| 5 | failed | 疲倦、坐下、躺下 |
| 6 | waiting | 等待、托腮、打盹 |
| 7 | running | 工作中的姿态轮换 |
| 8 | review | 观察与打趣 |

动画由参考绘制的关键姿态与少量位移组成，不是原片逐帧复制，也不是视频补帧。
`animation-manifest.json` 记录原设计时序；各宿主可能使用自己的播放速度。
本发布是 **legacy 8×9 图集**，没有新增 16 向 look 动作，不冒充新版 v2 角色。

## 仓库结构

```text
pets/              三套可直接使用的角色文件夹
sources/artwork/   六阶段中的高清生成原稿
sources/frames/    两套造型的透明切帧及相对坐标
sources/pixel/     保留的像素逻辑图集和调色板
sources/prompts/   制作提示词
scripts/           构建、校验、发行打包工具
docs/              安装、构建、画廊及项目参考说明
archive/metadata/  历史包的原始元数据
catalogue.json     版本映射、状态时序及像素校验指纹
index.html         可离线播放的预览页
```

## 参与与许可

欢迎改进安装文档、兼容性与构建工具，见 [CONTRIBUTING.md](CONTRIBUTING.md)。
工具代码和文档采用 [MIT](LICENSE)；角色及图片素材单独遵循 [ASSET_RIGHTS.md](ASSET_RIGHTS.md)，未取得官方角色授权。

展示结构参考 [VPet](https://github.com/LorisYounger/VPet) 与 [OpenPets](https://github.com/OpenPetsHQ/openpets)，
角色包格式参考 [Petdex](https://github.com/crafter-station/petdex)。没有复制上述项目的角色图片或程序代码。
