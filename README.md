# Scanner
前期信息搜集的自动化脚本
### 自定义脚本运行
在config_run 自定义需要的脚本的参数，脚本放于lib
### 目前支持的脚本
-webscanner<br>
args:<br>
&#8195;url:目标网站<br>
&#8195;type:网站脚本类型默认php<br>
&#8195;threads:线程<br>
&#8195;headers:自定义头部<br>
-google_hacking<br>
&#8195;search_key搜索关键词支持谷歌hack语法<br>
&#8195;numbers搜索网站数量<br>
&#8195;threads线程<br>
&#8195;output_file输出结果到文件<br>
&#8195;delay设置访问的延迟<br>
&#8195;show是否显示到终端<br>
&#8195;auto_use_sqlmap是否自动调用sqlmap<br>
&#8195;sqlmap_path调用sqlmap的路径<br>
