#Controller used for managing the listings list on /listings.mako
#
# Get Url parameters for use in the app
urlParams = {}
window.onpopstate = ->
  p = /\+/g
  search = /([^&=]+)=?([^&]*)/g
  decode = (s) ->
    return decodeURIComponent(s.replace(pl, " "))
  query = window.location.search.substring(1)
  while match = search.exec query
    urlParams[decode(match[1])] = decode(match[2])
  
ListingController = ($scope, $http) ->
  $scope.start = 0
  $scope.rows = 10
  $scope.listings = []
  
  $scope.getMore = ->
    baseUrl = "/listings.json?"
    for key, value of urlParams
      baseUrl += "&#{key}=#{value}"
    $http.get(baseUrl).success (data) ->
      for entry in data
        $scope.listings.push(entry)
      $scope.start += $scope.rows
  $scope.getMore()