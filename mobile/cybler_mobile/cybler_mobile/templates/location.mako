<%inherit file="head.mako" />
  
  <%block name="header_title">
  Choose your location
  </%block>

  
  <%block name="content">
    <ul data-role="listview">
      % for location in cities:
      <li>
      <a href="/listing?lat=${location['loc']['lat']}&lon=${location['loc']['lon']}">
        ${location['city']}
      </a>
      </li>
      % endfor
    </ul>
  </%block>