---
layout: post
title: 四级单词词频统计分析项目
date: 2018-07-26
categories:
- python
tags: [python,统计工具,数据库]
status: publish
type: post
published: true
meta:
  _edit_last: '1'
  views: '2'
---
## 起因
学校信工文化展示,我想起七个习惯的第一个积极主动，我就赶紧来了个程序  
- 终端上的钢琴（按键发声）**放弃，以后可能会捡起来**
- 人工智能艺术家（自己按大数据生成简谱简谱）**放弃，这个难，速成就和傻子一样**
- 最后选择**词频统计**，有类似分享的源码，还有苦短的python  

## 过程
- 花了不少时间找到源码
- 修改python版本
- 读了会儿英文peewee文档
- 费神思考没学过的数据库
- 拿命看别人的小型源码项目
- 补完源码作者的各种坑  

## 程序介绍  
这是一个单词频率统计程序 基于python3
- 自动批量收集文件中的英语单词 txt (utf-8)
- 统计排序保存到本地数据库voca.db
- 翻译英文得到中文解释
- 数据库文件提取得到csv表格EXCEL  

## 理解精进
- setting 和 models_exp 都是用来存储变量的（对象和数据类型）
- 初始化都放在main里了，仅1一次，所以其他文件引用的时候，都是拉取变量
- 外用接口1个 + 内部处理函数_init _build
- yield真有意思
- 原作者写的代码结构没那么清晰(也可能是我的代码经验不够)，所以非常难读懂
- 一个程序还是要分块把任务布置下去，面向对象也要有这种想法，一个用于分析的对象就分析，把数据拿出来，放到数据库处理对象里面去，甚至main函数可以写很多特殊函数的细节，但是每一个对象的每一个功能，我都希望是独立的存在，互相给接口
- 这个源码就属于耦合比较严重，main(work)主文件里，依赖的部件在分支中也依赖，不是一个root->各种独立的旁支的结构，而是类似网状
- 不过源代码作者引入的是作为变量的数据库对象和setting值
- 但是对于数据库的操作放进了analysis对象里面 我非常不舒服
- 对于数据库的操作应该放到数据库的对象里面 或者 数据库的操作对象里面
