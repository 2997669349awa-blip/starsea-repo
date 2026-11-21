#!/usr/bin/env python3
"""生成 spm 仓库 Packages 索引。扫描当前目录所有 *.spm.tar.gz，
读取各自 control 元数据，按包名排序输出 Packages 文件。"""
import glob, tarfile, os

out = []
for f in glob.glob('*.spm.tar.gz'):
    if f.startswith('tampered'):
        continue
    try:
        with tarfile.open(f, 'r:gz') as t:
            c = t.extractfile('control').read().decode()
    except Exception as e:
        print('skip', f, e)
        continue
    kv = {}
    for line in c.splitlines():
        if '=' in line:
            k, v = line.split('=', 1)
            kv[k] = v.strip().strip('"')
    out.append((kv.get('NAME', ''), kv.get('VERSION', ''),
                kv.get('DEPENDS', ''), f, kv.get('DESC', '')))

out.sort()
with open('Packages', 'w') as fh:
    for name, ver, dep, fn, desc in out:
        fh.write(f"Package: {name}\nVersion: {ver}\nDepends: {dep}\n"
                 f"Filename: {fn}\nDescription: {desc}\n\n")
print(f"generated Packages: {len(out)} packages")
for name, _, _, _, _ in out:
    print('  -', name)
