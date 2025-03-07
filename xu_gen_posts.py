import requests
from bs4 import BeautifulSoup
from xml.etree import ElementTree as ET
from datetime import datetime
import time
import os
import re

# 配置参数
SITEMAP_URL = "https://notes.mindcryst.com/blog/sitemap.xml"
OUTPUT_DIR = "./_posts"
HEADERS = {'User-Agent': 'Generator/1.0 (+https://github.com/yourusername)'}

def parse_sitemap(url):
    """解析sitemap.xml获取文章URL"""
    response = requests.get(url, headers=HEADERS)
    root = ET.fromstring(response.content)
    namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    return [url.text for url in root.findall('ns:url/ns:loc', namespace)]

def extract_content(article_url):
    """抓取文章内容并提取信息"""
    time.sleep(1)
    try:
        response = requests.get(article_url, headers=HEADERS)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 提取元数据
        title = soup.find('meta', {'property': 'og:title'}).get('content', '').strip()
        pub_time = soup.find('meta', {'property': 'article:published_time'})
        date = datetime.fromisoformat(pub_time['content']).strftime('%Y-%m-%d') if pub_time else datetime.now().strftime('%Y-%m-%d')
        
        # 提取正文（保留原始HTML格式）
        content_div = soup.find('div', class_='post-content')
        content = str(content_div) if content_div else ""

        return {
            'title': title,
            'date': date,
            'content': content,
            'url': article_url
        }
    except Exception as e:
        print(f"Error processing {article_url}: {str(e)}")
        return None

def generate_front_matter(post_data):
    """生成符合要求的YAML front matter"""
    return f"""---
layout: post
title: "{post_data['title']}"
date: {post_data['date']}
categories:
- 杂物间
tags: [我, 默认分类]
status: publish
type: post
published: true
meta:
  _edit_last: '1'
  views: '2'
  canonical_url: "{post_data['url']}"
---

"""

def generate_filename(post_data):
    """生成Jekyll标准文件名"""
    cleaned_title = re.sub(r'[^\w\u4e00-\u9fff\-]', ' ', post_data['title'])
    cleaned_title = re.sub(r'\s+', '-', cleaned_title).lower()[:50]
    return f"{post_data['date']}-{cleaned_title}.md"

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    article_urls = parse_sitemap(SITEMAP_URL)
    print(f"Found {len(article_urls)} articles")
    
    existing_files = set(os.listdir(OUTPUT_DIR))
    
    for idx, url in enumerate(article_urls):
        print(f"Processing {idx+1}/{len(article_urls)}: {url}")
        
        # 生成临时文件名用于检查
        temp_data = {'title': url.split('/')[-1], 'date': '2000-01-01'}
        temp_filename = generate_filename(temp_data)
        if any(url.split('/')[-1] in f for f in existing_files):
            print(f"  → 已存在，跳过")
            continue
            
        post_data = extract_content(url)
        if not post_data: continue
        
        filename = generate_filename(post_data)
        if filename in existing_files:
            print(f"  → 文件已存在: {filename}")
            continue
            
        # 构建完整内容
        full_content = generate_front_matter(post_data)
        full_content += f"## {post_data['title']}\n\n"
        full_content += f"{BeautifulSoup(post_data['content'], 'html.parser').text[:500]}...\n\n"
        full_content += f"**阅读完整文章**: [{post_data['title']}]({post_data['url']})"
        
        # 保存文件
        with open(os.path.join(OUTPUT_DIR, filename), 'w', encoding='utf-8') as f:
            f.write(full_content)
        
        existing_files.add(filename)
    
    print(f"生成完成，文件保存在 {OUTPUT_DIR}")

if __name__ == "__main__":
    main()