<%doc>
This is a single view for a listing. Contains a 
single link to a slideshow gallery (can go back)
</%doc>
<%inherit file="./head.mako" />
<%block name="head_js">

</%block>

<%block name="left-head-buttons">
<a href="/listings?lat=${location["loc"]["lat"]}&lon=${location["loc"]["lon"]}"
   data-icon="arrow-l">
  Back
</a>
</%block>

<%block name="header_title">
    ${location["city"].title()}
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
    jQuery("#preview").on("tap", function(event){
      window.location.href = "/listing/${listing["_id"]}/gallery";
    });
    clearInterval(interval);
  }  
};

interval = setInterval(check, 1000); //Check every second
</script>
</%block>
