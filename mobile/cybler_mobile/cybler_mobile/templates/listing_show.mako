<%doc>
This is a single view for a listing. Contains a 
single link to a slideshow gallery (can go back)
</%doc>
<%inherit file="./head.mako" />
<%block name="head_js">
<script type="text/javascript" src="/static/js/camera.min.js"></script>
<script type="text/javascript">
jQuery(".camera-wrap").camera()
</script>
</%block>

<%block name="header_title">
  ${listing["title"]}
</%block>

<%block name="content">
<a rel="external" href="${listing["url"]}"><h2>${listing["title"]</h2></a>
${listing["createdOn"]}
<hr/>
% if listing["images"]:
<a href="/listing/images/${listing["_id"]}">
  <div class="camera_wrap">
  %for image in listing["images"]:
    <div data-src="${image}"></div>
  %endfor
  </div>
</a>
%endif

<p>${listing["description"]}</p>
</%block>