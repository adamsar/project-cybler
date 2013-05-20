<!DOCTYPE html>
  <html>
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black">
    <title>Project Cybler</title>
    <link rel="stylesheet" href="/static/css/jquery.mobile-1.3.1.min.css">

    <!-- jQuery and jQuery Mobile -->
    <script src="/static/js/jquery-1.8.3.min.js"></script>
    <script src="/static/js/jquery.mobile-1.3.1.min.js"></script>
  
  <script type="text/javascript">
  <%block name="head_js"/>
  </script>
  
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
