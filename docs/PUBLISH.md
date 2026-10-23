# GitHub 发布

所有运行代码与角色文件均保存在仓库，普通用户直接下载源码 ZIP 即可离线预览。
维护者可以用 GitHub CLI 发布。请先在自己的终端完成 `gh auth login`，不要把访问令牌写进仓库。

```sh
python scripts/build.py
python scripts/release.py
git push origin main
gh release create v<版本号> dist/*.zip dist/SHA256SUMS.txt --target main --title "摩羯 Capri v<版本号>" --notes-file .github/RELEASE_NOTES.md
```

版本号取 `catalogue.json` 的 `version`，发布前同步更新 `CHANGELOG.md` 与 `.github/RELEASE_NOTES.md`。
首次建库可用 `gh repo create capri-desktop-pet --public --source . --remote origin --push`；
如果同名仓库已经存在，先核对其内容，不要覆盖或强推。
Windows PowerShell 不会替所有原生命令展开通配符；可在发行命令中显式列出五个 ZIP 和校验和文件。
自动化流程作为模板保存在 `.github/workflow-templates/`，初始发布不要求开启 GitHub Actions。
