<!DOCTYPE html>
<html>
<head>
	<title>seebug scrapy test</title>
	<meta charset="utf-8">
	<link rel="stylesheet" href="reset.css">
	<link rel="stylesheet" href="main.css">
</head>
<body>
	<div id="sidebar"><!-- 侧边栏部分 -->
	<div id="sidbar-ccontent" class="inner">
		<h2 class="blog-title">
			<a href="#">Paper</a>
		</h2>
		<h3 class="blog-descrition">安全技术精粹-scrapy</h3>
		<form id="search" action="#">
      		<button type="submit" style="background: #13313f; border: #13313f; position: absolute; right: -4px; margin-top: -3px;">
        	<i class="fa fa-search search-button" style="position: absolute;right:10px; margin-top:6px;"> </i>
      		</button>
      		<input id="search-field" name="keyword" value="" placeholder="Search">
    	</form>
    </div><!-- 侧边栏结束 -->
    <main><!-- 内容模块开始 -->
    	<div class="main-inner">
    		<article class="post">
    			<?php
    				$num = 0;
    				$m = new MongoClient();
    				$collection = $m->paper->article;
    				$cursor = $collection->find();
    				foreach ($cursor as $document) {
    					$num += 1;
    					echo '<h5><a href="#">'.$num.'、'.$document['title'].'</a></h5>';
    					echo '<p>category:'.$document['category'].'</p>';
    					echo  '<p>time:'.$document['time'].'</p>';
    				}
    			?>		 			
  			</article>
    	</div>
    </main><!-- 内容模块结束 -->
</body>
</html>