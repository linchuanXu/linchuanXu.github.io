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


def generate_readme(articles):
    """生成或更新README.md文件，包含所有文章的链接"""
    readme_path = "README.md"  # 直接放到当前目录
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write("# 文章目录\n\n")
        f.write("以下是本站所有文章的目录，点击标题即可阅读全文：\n\n")
        for article in articles:
            f.write(f"- [{article['title']}]({article['url']}) - {article['date']}\n")
        f.write("\n\n---\n\n*本目录自动生成，最后更新时间：{}*".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    article_urls = parse_sitemap(SITEMAP_URL)
    print(f"Found {len(article_urls)} articles")
    
    articles = []  # 用于存储所有文章信息，用于生成README.md
    
    for idx, url in enumerate(article_urls):
        print(f"Processing {idx+1}/{len(article_urls)}: {url}")
            
        post_data = extract_content(url)
        if not post_data: continue
        
        # 构建完整内容
        full_content = generate_front_matter(post_data)
        full_content += f"## {post_data['title']}\n\n"
        full_content += f"{BeautifulSoup(post_data['content'], 'html.parser').text[:500]}...\n\n"
        full_content += f"**阅读完整文章**: [{post_data['title']}]({post_data['url']})"
        
        # 保存文章文件
        filename = generate_filename(post_data)
        with open(os.path.join(OUTPUT_DIR, filename), 'w', encoding='utf-8') as f:
            f.write(full_content)
        
        # 将文章信息添加到列表中
        articles.append(post_data)
    
    # 生成README.md
    generate_readme(articles)
    
    print(f"生成完成，文件保存在 {OUTPUT_DIR}")

if __name__ == "__main__":
    main()