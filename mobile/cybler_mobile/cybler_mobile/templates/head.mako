<%doc>
Base template that most templates inherit (excluding the ones that 
don't clearly).
</%doc>
<!DOCTYPE html>
  <html ng-app>
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black">
    <title>Project Cybler</title>

    <link rel="stylesheet" href="/static/css/themes/cybler.min.css" />
    <link rel="stylesheet" href="http://code.jquery.com/mobile/1.3.1/jquery.mobile.structure-1.3.1.min.css" />
    <link rel="stylesheet" href="/static/css/camera.css"/>
    <link rel="stylesheet" href="/static/css/cybler.css"/>
    <link rel="stylesheet" href="/static/css/jqm-icon-pack-2.0-original.css"/>
    <!-- Jquery 1.8.3 is needed for the camera plugin -->
    <script src="http://code.jquery.com/jquery-1.8.3.min.js"></script>
    <script src="http://code.jquery.com/mobile/1.3.1/jquery.mobile-1.3.1.min.js"></script>    
    <script type="text/javascript" src="/static/js/angular.min.js"></script>
    <script type="text/javascript" src="/static/js/angular.adapter.min.js"></script>
    <script type="text/javascript" src="/static/js/jquery.easing.1.3.js"></script>
    <script type="text/javascript" src="/static/js/camera.js"></script>
    <script type="text/javascript" src="/static/js/cybler.js"></script>
    <%block name="head_js"/>
</head>
  
<body>
  <div data-role="page" id="location" data-theme="c">
    <div data-role="header">
      <%block name="left_head_buttons"/>
      <h1>
      <%block name="header_title"/>
      </h1>  
      <%block name="right_head_buttons"/>
    </div>
    <div data-role="content">
     <%block name="content"/>  
    </div>
    <div data-role="footer" data-id="foot" data-position="fixed">
      <div data-role="navbar" data-iconpos="bottom">
        <ul>
            <li>
              <a rel="external" data-ajax="false" data-icon="home" href="/">

              </a>
            </li>
            <li>
              <a data-icon="grid" href="/location">

              </a>
            </li>
            <%block name="nav_bar_items"/>
            <li>
              <a data-icon="info" href="/about">
              </a>
            </li>
        </ul>
      </div>
    </div>
  </div>
</body>
  
</html>
