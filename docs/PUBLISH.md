# GitHub 发布

所有运行代码与角色文件均保存在仓库，普通用户直接下载源码 ZIP 即可离线预览。
维护者可以用 GitHub CLI 发布。请先在自己的终端完成 `gh auth login`，不要把访问令牌写进仓库。

```sh
python scripts/build.py
python scripts/release.py
gh repo create capri-desktop-pet --public --source . --remote origin --push
git tag v1.0.0
git push origin v1.0.0
gh release create v1.0.0 dist/*.zip dist/SHA256SUMS.txt --title "摩羯 Capri v1.0.0" --notes-file .github/RELEASE_NOTES.md
```

创建仓库命令要求本地已经有提交；如果同名仓库已经存在，先核对其内容，不要覆盖或强推。
Windows PowerShell 不会替所有原生命令展开通配符；可在发行命令中显式列出五个 ZIP 和校验和文件。
自动化流程作为模板保存在 `.github/workflow-templates/`，初始发布不要求开启 GitHub Actions。
