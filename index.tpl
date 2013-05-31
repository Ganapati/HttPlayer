<!DOCTYPE html>
<html>
	<head>
		<title>Player</title>
		<link type="text/css" rel="stylesheet" href="static/css/reset.css" />
		<link type="text/css" rel="stylesheet" href="static/css/player.css" />
		<link type="text/css" rel="stylesheet" href="static/css/style.css" />
		<script src="/static/js/jquery.min.js" ></script>
		<script src="/static/js/script.js" ></script>
	</head>
	<body>
		<div id="container">
			<audio id="player" src=""></audio>
			<div class="plyr_holder">  
  				<div class="plyr_img animated bounceInDown">
    				<img src="/static/images/default.png" alt="thumb" id="thumbnail"/>
  				</div>
  				<div class="plyr_details">
    				<ul>
      					<li><h1 class="title" id="artist"></h1></li>
      					<li class="song" id="title"></li>
      					<li class="album" id="album"></li>
    				</ul>
  					</div>
  					<div class="plyr_control">
    					<ul>
      						<li><a class="pleft"></a></li>
    	  					<li><a class="pplay" id="ppButton"></a></li>
      						<li><a class="pright"></a></li>
	      					<li>
	      						<div class="ptime">
    	    						<span class="pslider"></span>
        							<span class="pslider_dot"></span>
      							</div>
      						</li>
							<li class="volume">
								<span class="pvolume"></span>
								<div class="volumeBar">
    	    						<span class="psliderVolume"></span>
        							<span class="pslider_dotVolume"></span>
								</div>
							</li>
    					</ul>
  					</div>
				</div>
			
			<div id="file">
				<div id="filter">
					<select id="filterGenres"></select>
					<select id="filterArtists"></select>
					<input id="filterField" type="text" />
					<span id="filterBtn">Filter</span>
					<span id="filterClearBtn">Clear</span>
				</div>
				<div id="playlist">
					<table border="1" id="songList">
					</table>
				</div>
			</div>
		</div>
	</body>
</html>
