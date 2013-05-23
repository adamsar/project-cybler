<%doc>
This is a single view for a listing. Contains a 
single link to a slideshow gallery (can go back)
</%doc>
<%inherit file="./head.mako" />
<%block name="head_js">
<link rel="stylesheet" href="/static/css/camera.css"/>
<script type="text/javascript" src="/static/js/jquery.easing.1.3.js"></script>
<script type="text/javascript" src="/static/js/camera.js"></script>
</%block>

<%block name="header_title">
  ${listing["title"]}
</%block>

<%block name="content">
<a rel="external" href="${listing["url"]}"><h2>${listing["title"]}</h2></a>
${listing["createdOn"]}
<hr/>
% if listing["images"]:
<div class="camera_wrap" id="preview">
  %for image in listing["images"]:
    <div data-src="${image}"></div>
  %endfor
</div>
%endif

<p>${listing["description"]}</p>
<script type="text/javascript">
var interval = null;
var check = function(){
  if($(".cameraContents").length == 0){
    jQuery("#preview").camera();
  }else{
    clearInterval(interval);
  }  
};

interval = setInterval(check, 2000); //Check every 2 seconds
</script>
</%block>