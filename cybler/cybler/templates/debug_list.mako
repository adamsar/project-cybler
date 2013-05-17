<html>
  <head>
    <title>Dyre Wolf rock!</title>
  </head>
  <body>
  Results: <br/>
  <ul>
  % for entry in listings:
    <li>${entry["title"]}</li>
  % endfor
  </ul>
  </body>
</html> 