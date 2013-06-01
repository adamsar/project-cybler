<%inherit file="head.mako" />
  
  <%block name="header_title">
  Choose your location
  </%block>

  
  <%block name="content">
    <ul data-role="listview">
      % for location in locations:
      <li>
      <a href="/listing?city=${location.city}">
        ${location['city'].title()}
      </a>
      </li>
      % endfor
    </ul>
  </%block>
