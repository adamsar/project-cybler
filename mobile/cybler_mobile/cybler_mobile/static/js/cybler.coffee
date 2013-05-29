#Controller used for managing the listings list on /listings.mako

ListingController = ($scope, $http) ->
  $scope.start = 0
  $scope.rows = 10
  $scope.listings = []
  
  $scope.getMore = ->
    baseUrl = "/listings.json?start=#{$scope.start}&rows=#{$scope.rows}"
    if $scope.queryParams
      baseUrl += "&#{queryParams}"
    $http.get(baseUrl).success (data) ->
      for entry in data
        $scope.listings.push(entry)
      $scope.start += $scope.rows
  $scope.getMore()