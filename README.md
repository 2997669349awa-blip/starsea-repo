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

## 包清单

### 开发工具与运行环境（ARM64 官方/上游二进制）

| 包名 | 版本 | 说明 | 提供的命令 |
|------|------|------|-----------|
| `python3` | 3.15.2 | Python 官方 standalone 构建，自带 pip | `python3` `python` `pip3` |
| `nodejs` | 26.13.1 | Node.js LTS（nodejs.org 官方），自带 npm/npx/corepack | `node` `npm` `npx` `corepack` |
| `java` | 25.0.5 | Eclipse Temurin JRE 25 LTS | `java` `keytool` |
| `gcc` | 12.2.0 | GCC 工具链（Debian 官方，含 as/ld/头文件） | `gcc` `cc` `cpp` `as` `ld` |
| `mysql-client` | 10.11.18 | MariaDB/MySQL 兼容命令行客户端 | `mysql` `mysqldump` `mysqladmin` |

> 安装后命令位于 `/usr/local/bin`（默认在 PATH 中），程序主体位于 `/opt/<name>`。
>
> 说明：MySQL/MariaDB **服务端**官方二进制超过 900MB，超出 GitHub 单文件上限，故本源提供的是**客户端**（可连接任意 MySQL/MariaDB 服务器）。Python/Node/Java/GCC 均为对应上游的官方最新版 ARM64 构建，全部为真实可运行二进制。

### 常用命令行工具（Debian bookworm 官方 ARM64 包，自包含依赖）

| 包名 | 版本 | 说明 | 提供的命令 |
|------|------|------|-----------|
| `git` | 2.39.5 | 分布式版本控制 | `git` |
| `curl` | 7.88.1 | URL 传输工具 | `curl` |
| `wget` | 1.21.3 | 网络下载工具 | `wget` |
| `rsync` | 3.2.7 | 文件同步 | `rsync` |
| `openssh-client` | 9.2p1 | SSH/SCP/SFTP 客户端 | `ssh` `scp` `sftp` `ssh-keygen` |
| `jq` | 1.6 | JSON 命令行处理器 | `jq` |
| `tmux` | 3.3a | 终端复用器 | `tmux` |
| `htop` | 3.2.2 | 交互式进程查看器 | `htop` |
| `btop` | 1.2.13 | 系统资源监视器 | `btop` |
| `ripgrep` | 13.0.0 | 高速递归搜索 | `rg` |
| `fzf` | 0.38.0 | 命令行模糊查找 | `fzf` |
| `tree` | 2.1.0 | 目录树显示 | `tree` |
| `sqlite3` | 3.40.1 | SQLite 数据库命令行 | `sqlite3` |
| `vim` | 9.0.1378 | Vim 编辑器 | `vim` `vi` |
| `nano` | 7.2 | 简易文本编辑器 | `nano` |
| `zsh` | 5.9 | Zsh shell | `zsh` |
| `make` | 4.3 | GNU Make 构建工具 | `make` |
| `ninja` | 1.11.1 | Ninja 构建系统 | `ninja` |
| `cmake` | 3.25.1 | CMake 构建生成器 | `cmake` `ctest` |
| `unzip` | 6.0 | ZIP 解压 | `unzip` |
| `zip` | 3.0 | ZIP 压缩 | `zip` |

> 以上 21 个工具均来自 Debian bookworm 官方 arm64 仓库，运行时依赖的第三方共享库已一并打包进各自 spm 包，解压即可运行，不依赖宿主机预装额外库。全部经过 qemu-aarch64 实机模拟运行验证。

### 基础与演示包

`calc` `cowsay` `fortunes` `gcdemo` `hello` `hello-pro` `nettool` `sysinfo` `sysmon`

当前仓库共 **35 个包**。

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
