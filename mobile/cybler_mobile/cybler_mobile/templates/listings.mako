<%inherit file="head.mako" />
  <%block name="header_title">
    Your listings
  </%block>  
<%block name="content">
  <ul class="listings" data-role="listview" data-theme="d">
  % for listing in listings:
    <li>
      <a href="/listing/${listing['_id']}">
        % if listing.get('images'):
            <img src="${listing['images'][0]}" />
        % else:
           <img src="/static/img/question.png" />
        % endif
        <h2>${listing['title']}</h2>
        <p>${listing['description']}</p>
      </a>
    </li>
  % endfor
  </ul>
</%block>  