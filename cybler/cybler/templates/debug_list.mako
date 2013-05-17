<html>
  <head>
    <title>Dyre Wolf rock!</title>
  </head>
  <body>
  Results: <br/>
  <ul>
  % for entry in listings:
    <li>
      <a href="${entry["url"]}">${entry["title"]}</a>
      <hr/>
      <div>
        ${entry["description"]}
      </div>
      <div style="color: red;">
        From: ${entry["type"]}
      </div>
      <div>
        Images:
        <ul>
          % for image in entry.get("images", []) or []:
            <li><img src="${image.replace("'", "").replace("[", "")}"/></li>
          % endfor
        </ul>
      </div>
    </li>
  % endfor
  </ul>
  </body>
</html> 