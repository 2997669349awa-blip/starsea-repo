# StarSeaLinux 官方 spm 软件源

这是 StarSeaLinux 的**官方原生软件仓库源**，托管在 GitHub，通过 `raw.githubusercontent.com` 直接分发。

## 为什么需要自己的源

spm 使用自己的包格式（`.spm.tar.gz` + RSA-2048 签名），与 Debian/Ubuntu 的 `.deb`、CentOS 的 `.rpm` **不兼容**。因此阿里云/腾讯云等公共镜像无法作为 spm 源使用。本仓库提供原生 spm 包，让 `spm install` 真正可用。

## 使用方法（在 StarSeaLinux 系统内）

```sh
# 1. 确认源已配置（默认已写入 /etc/spm/sources.list）
spm source

# 2. 更新索引
spm update

# 3. 搜索 / 安装
spm search
spm install hello
spm install sysinfo        # 会自动安装依赖 hello
spm list
```

也可以手动把下面一行加入 `/etc/spm/sources.list`：

```
https://raw.githubusercontent.com/2997669349awa-blip/starsea-repo/main
```

## 目录结构

```
Packages                  # 包索引（spm update 拉取这个文件）
*.spm.tar.gz              # 签名软件包（spm install 下载这些）
pubkey.n                  # RSA 公钥模数（e=65537）
gen-packages.py           # 索引生成脚本（加包后运行）
README.md
```

## 包格式与安全

每个 `.spm.tar.gz` 内含：

| 文件 | 说明 |
|------|------|
| `control` | 元数据：NAME / VERSION / DEPENDS / CONFLICTS / DESC / SIGTYPE |
| `payload.tar.gz` | 实际文件树 |
| `payload.sig` | RSA-2048 / PKCS#1 v1.5 / SHA-256 签名（对 payload.tar.gz 签名）|

安装时 spm 用 `pubkey.n`（模数，e=65537）验签，**签名不通过拒绝安装**。私钥不在系统内，也不在本仓库。`tampered.spm.tar.gz`（篡改测试样本）故意不发布。

## 维护：添加新包后重建索引

```sh
python3 gen-packages.py
git add Packages *.spm.tar.gz && git commit -m "add package: xxx" && git push
```

> 注意：GitHub raw 有 CDN 缓存，`push` 后约 1-5 分钟生效。
