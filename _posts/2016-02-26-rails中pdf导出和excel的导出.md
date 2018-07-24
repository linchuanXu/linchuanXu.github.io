---
layout: post
title:  "rails中pdf导出和excel的导出"
date:   2016-02-26 15:41:00
categories: rails
comments: true
---

rails中有多种导出pdf的方法，今天用到一种做个记录：

参考例子：https://github.com/luciditydigital/wicked-pdf-sample-app

项目中使用的gem:

gem 'wicked_pdf'

gem 'wkhtmltopdf-binary'  #依赖工具

环境配置

在不同的服务器环配置相应环境：

地址是： http://wkhtmltopdf.org/downloads.html

在controller中:
{% highlight ruby %}
def print
  @training_course = TrainingCourse.find(params[:id])
    respond_to do |format|
      format.html
      format.pdf do
        render :pdf => @training_course.name,
               :template => "training_courses/print.pdf.erb",
﻿               :layout => 'pdf.html.erb'
      end
    end
  end
end
{% endhighlight %}

在view中:

layouts/pdf.html.erb:

{% highlight ruby %}
<!DOCTYPE html>
<html>
  <head>
    <title>上海高等职业教育师资公共培训</title>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <%= wicked_pdf_stylesheet_link_tag 'application', media: 'all', 'data-turbolinks-track' => true %>
  </head>
  <body class="<%= controller.controller_path.gsub('/','__') + '__' + controller.action_name %>">
    <%= yield %>
  </body>
</html>
{% endhighlight %}

print.html.erb和print.pdf.erb内容相同。

打印按钮：

{% highlight ruby %}
<%= link_to print_training_course_path(training_course, format: 'pdf'), title: "打印" do%>打印报名表 <% end %>
{% endhighlight %}