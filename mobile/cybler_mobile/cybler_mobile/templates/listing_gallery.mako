<%doc>
This is an image gallery for a listing. A simple interface for
viewing all images for a listing
</%doc>
<%inherit file="./head.mako"/>
<%block name="head_js">
<script type="text/javascript" src="/startic/js/klass.min.js"></script>
<script type="text/javascript" src="/startic/js/code.photoswipe-3.0.4.min.js"></script>
<script type="text/javascript">
$(document).ready(function(){
  var photoSwiped = $("#gallery a").photoSwipe({enableMouseWheel: false});
});
</script>
</%block>

<%block name="header_title">
Gallery for %{listing["title"]}
</%block>

<%block name="content">
<ul id="gallery">
% for image in listing["images"]:
  <li><a href="${image}"><img src="${image}"/></a></li>
% endfor
</ul>
</%block>