#Controller used for managing the listings list on /listings.mako
#
# Get Url parameters for use in the app

getUrlVars = ->
  vars = []
  hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&')
  for hash in hashes
    hash = hash.split "="
    vars[hash[0]] = hash[1]
  return vars
urlParams = getUrlVars()
  
ListingController = ($scope, $http) ->
  $scope.start = 0
  $scope.rows = 10
  $scope.listings = []
  
  $scope.getMore = ->
    baseUrl = "/listings.json?start=#{$scope.start}&rows=#{$scope.rows}"
    for key, value of urlParams
      baseUrl += "&#{key}=#{value}"
    $http.get(baseUrl).success (data) ->
      for entry in data
        $scope.listings.push(entry)
      $scope.start += $scope.rows
  $scope.getMore()