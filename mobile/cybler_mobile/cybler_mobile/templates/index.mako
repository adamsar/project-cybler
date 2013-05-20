<!DOCTYPE html>
  <html>
    <head>
      <style>
    .title-box {
      -moz-box-shadow: 0 1px 3px /*{global-box-shadow-size}*/       rgba(0,0,0,.2) /*{global-box-shadow-color}*/;
      -webkit-box-shadow: 0 1px 3px /*{global-box-shadow-size}*/    rgba(0,0,0,.2) /*{global-box-shadow-color}*/;
      box-shadow: 1 1px 3px /*{global-box-shadow-size}*/     rgba(0,0,0,.2) /*{global-box-shadow-color}*/;
      border: 1px solid #bbb /*{d-bup-border}*/;
      padding: 10px;
      width: 80%;      
      }
      </style>
  
      <script src="/static/js/jquery-1.8.3.min.js"></script>
      <script>
          jQuery(window).ready(function(){
            initiate_geolocation();
          });
          function initiate_geolocation() {
              navigator.geolocation.getCurrentPosition(handle_geolocation_query,handle_errors);
          }
          function handle_errors(error)
          {
            window.location.href = "/location"
          }
          function handle_geolocation_query(position){
            window.location.href = "/listing?lat=" + position.coords.latitude +
                                  "&lon=" + position.coords.longitude +
                                  "&start=0";
          }
      </script>
    </head>
    <body>
      <div>
    <center>
      <img src="/static/img/logo.png"/>
      <br/>
       <div class="title-box">
        Find a friend tonight!
       </div>
    </center>
      </div>
    </body>
  </html>