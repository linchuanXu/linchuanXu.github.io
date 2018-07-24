---
layout: post
title:  "rails中scope的用法"
date:   2016-04-14 16:30:00
categories: rails
comments: true
---

简单的单表中使用scope:

{% highlight ruby %}
class Post < ActiveRecord::Base
  scope :is_active, {where(status: 'active')}
  scope :has_content, {joins(:comment).where("comments.content is not null")}
end

传参数的scope

{% highlight ruby %}
class Shirt < ActiveRecord::Base
   scope :yellow, lambda {|color| where(color: color)}         #旧写法
   scope :yellow, (color){where(color: color)}                 #新写法
end
{% endhighlight %}

这样调用Shirt.yellow("yellow")将返回所有颜色为yellow的Shirt集合

注意 当scope定义时就被evaluated了，而不是当它被使用时，所以下面的将是错误的

{% highlight ruby %}
class Post < ActiveRecord::Base
  scope :recent, where('published_at >= ?', Time.now - 1.week)
end
{% endhighlight %}

上面这个scope将frozen成Time.now的value当Post类被定义时,所以查询的内容一致不会变化，正确的方式是使用lambda,

这将在该scope每次被调用时re-evaluate一下。

{% highlight ruby %}
class Post < ActiveRecord::Base
    scope :recent, lambda {where('published_at >= ?', Time.now - 1.week)}
end
{% endhighlight %}

综上理解：也就是当我们传入的参数如果是一个变化的量时，要使用lambda，这样在每次调用时都会re-evaluted一下