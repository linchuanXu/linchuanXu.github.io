#!/bin/bash

# 生成文章
python xu_gen_posts.py

# 添加所有更改到 Git
git add .

# 提交更改（使用当前时间作为提交信息）
git commit -m "自动更新文章目录和内容 - $(date '+%Y-%m-%d %H:%M:%S')"

# 推送到远程仓库
git push

echo "文章已生成并推送到 Git 仓库！"