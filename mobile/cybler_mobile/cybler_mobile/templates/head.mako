<!DOCTYPE html>
  <html>
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black">
    <title>Project Cybler</title>

    <link rel="stylesheet" href="/static/css/themes/cybler.min.css" />
    <link rel="stylesheet" href="http://code.jquery.com/mobile/1.3.1/jquery.mobile.structure-1.3.1.min.css" />
    <link rel="stylesheet" href="/static/css/camera.css"/>
    <!-- Jquery 1.8.3 is needed for the camera plugin -->
    <script src="http://code.jquery.com/jquery-1.8.3.min.js"></script>
    <script src="http://code.jquery.com/mobile/1.3.1/jquery.mobile-1.3.1.min.js"></script>    
    <script type="text/javascript" src="/static/js/jquery.easing.1.3.js"></script>
    <script type="text/javascript" src="/static/js/camera.js"></script>

    <%block name="head_js"/>
</head>
  
<body>
  <div data-role="page" id="location" data-theme="c">
    <div data-role="header">
      <h1>
      <%block name="header_title"/>
      </h1>  
    </div>
    <div data-role="content">
     <%block name="content"/>  
    </div>
  </div>
</body>
  
</html>
