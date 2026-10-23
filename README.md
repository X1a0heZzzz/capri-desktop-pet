<div align="center">

# 摩羯 · Capri Desktop Pet

**一只粉红色的小伙伴，六个制作阶段，三套可用桌宠包。**

[English](README.en.md) · **[下载最新版](https://github.com/X1a0heZzzz/capri-desktop-pet/releases/latest)** · [版本画廊](#六个制作阶段) · [安装说明](docs/INSTALL.md) · [离线预览源码](index.html) · [角色素材说明](ASSET_RIGHTS.md)

![清晰版九种状态轮播](docs/previews/capri-clear.gif)

</div>

保留摩羯从初稿、休息姿态、动漫细化到 Q 版原稿、像素化和清晰桌宠的全部现存制作阶段。
默认推荐 **Q版清晰原稿**：保留头发纹理、白色/绿色眼框、嘴形，以及托腮、侧躺、打趣等姿态。

> **v1.1 清晰版美术完善**：重新编排九种动作，适配 Codex / Petdex 默认约 1 秒一轮的播放速度——
> 待机改为呼吸 + 眨眼，不再在六个姿势间闪切；移动时朝向和视线跟随方向；清掉了原稿抠图留下的暗色污边和紫边。
> 详见[版本记录](CHANGELOG.md)。

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

**⑥ 清晰版（v1.1）**

| 行 | 状态 | 内容 |
| --- | --- | --- |
| 0 | idle | 悬浮呼吸、碎发飘动、眨一次眼 |
| 1 / 2 | running-right / running-left | 视线朝前进方向，前倾小跳两步；向左为逐帧镜像 |
| 3 | waving | 抬手打招呼，身体左右摆 |
| 4 | jumping | 下蹲蓄力 → 举手跳起 → 落回原基线 |
| 5 | failed | 吓一跳（白眼框）→ 垂头 → 跪坐 → 侧躺摆烂 |
| 6 | waiting | 托腮发呆，轻微呼吸并眨眼 |
| 7 | running | 手忙脚乱地上下颠（工作中，不是跑步） |
| 8 | review | 眨眼指人，歪头点评 |

![清晰版全部状态](docs/previews/capri-clear-states.png)

所有帧都来自原稿姿势，没有重新绘制角色；新增的只有整体位移、倾斜、挤压拉伸、碎发独立飘动、
镜像，以及在原有眼睛位置上画的闭眼线。③⑤ 两套仍是 v1.0 的关键姿态编排，按慢速时序设计，
在默认速度的宿主里会切换得很快，推荐使用 ⑥。

三套包的 `animation-manifest.json` 记录设计时序；Codex / Petdex 通常使用自己的默认速度
（待机约 280/110/110/140/140/320 毫秒），⑥ 的时序与之保持一致。
本发布是 **legacy 8×9 图集**，没有新增 16 向 look 动作，不冒充新版 v2 角色。

## 仓库结构

```text
pets/              三套可直接使用的角色文件夹
sources/artwork/   六阶段中的高清生成原稿
sources/frames/    两套造型的透明切帧及相对坐标
sources/pixel/     保留的像素逻辑图集和调色板
sources/prompts/   制作提示词（含 Q 版两张原稿和面部修订）
scripts/           构建、动作编排、预览渲染、校验、发行打包工具
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
