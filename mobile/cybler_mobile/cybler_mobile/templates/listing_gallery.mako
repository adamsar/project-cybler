<%doc>
This is an image gallery for a listing. A simple interface for
viewing all images for a listing
</%doc>
<%inherit file="./head.mako"/>
<%block name="head_js">
<script type="text/javascript" src="/static/js/klass-min.js"></script>
<script type="text/javascript" src="/static/js/code.photoswipe-3.0.5.min.js"></script>
<script type="text/javascript">
$(document).ready(function(){
  var photoSwiped = $("#gallery a").photoSwipe({enableMouseWheel: false, zIndex: 0});
  photoSwiped.show(0);
});
</script>
</%block>C

<%block name="left_head_buttons">
<a href="/listing/${listing["_id"]}"
   data-icon="arrow-l">
  Back
</a>
</%block>

<%block name="header_title">
Gallery
</%block>

<%block name="content">
<ul class="hidden" id="gallery">
% for image in listing["images"]:
  <li><a rel="external" href="${image}"><img src="${image}"/></a></li>
% endfor
</ul>
</%block>
