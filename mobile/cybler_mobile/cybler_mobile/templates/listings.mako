<%inherit file="head.mako" />
<%block name="header_title">
    ${location["city"].title()}
</%block>

<%block name="content">
<div ng-init="queryParams = \"${queryParams}\"" >
  <ul ng-controller="ListingController" 
    class="listings" 
    data-role="listview" 
    data-theme="d">

  <li ng-repeat="listing in listings">
    <a href="/listing/{{listing.id}}">      
      <img ng-src="{{listing.image}}" />
      <h2>{{listing.title}}</h2>
      <p>{{listing.description}}</p>
      <p class="ui-li-aside">
        <strong>
            {{listing.createdOn}}
        </strong>
      </p>
    </a>
  </li>

  <li class="centered" data-role="list-divider" 
      role="footing" data-theme="a" ng-click="getMore()">
    More
  </li>
</ul>
</div>
</%block>
