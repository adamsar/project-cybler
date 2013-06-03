<%doc>
This is a single view for a listing. Contains a 
single link to a slideshow gallery (can go back)
</%doc>
<%inherit file="./head.mako" />
<%block name="head_js">

</%block>

<%block name="left_head_buttons">
<a href="/listing?city=${listing["contact"]["city"]}"
   data-icon="arrow-l">
  Back
</a>
</%block>

<%block name="header_title">
    ${listing["contact"]["city"].title()}
</%block>

<%block name="content">
<a rel="external" href="${listing["url"]}"><h2>${listing["title"]}</h2></a>
${listing["created_on"]}
<hr/>
% if listing["images"]:
<div class="camera_wrap" id="preview">
  %for image in listing["images"]:
    <div data-src="${image}"></div>
  %endfor
</div>
%endif

% for paragraph in listing["description"].split("\n"):
<p>${paragraph}</p>
% endfor 

<script type="text/javascript">
var interval = null;
var check = function(){
  if($(".cameraContents").length == 0){
    jQuery("#preview").camera({playPause: false, time: 0, transPeriod: 0, pagination: false});
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

<%block name="navbar_items">
% if listing.get("contact", {}).get("phone_number"):
<!-- Include the phone number if it's a valid listing -->
<li>
  <a data-icon="phone" href="tel:${listing['contact']['phone_number']}">
  </a>
</li>
% endif
% if listing.get("email"):
<!-- Include the phone number if it's a valid listing -->
<li>
  <a data-icon="email" href="mailto:${listing['email']}">
  </a>
</li>
% endif
</%block>
