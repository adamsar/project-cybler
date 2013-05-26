#Controller used for managing the listings list on /listings.mako
getListings = (start, rows, lat, lon) ->
  
ListingController = ($scope, $http) ->
  $scope.start = 0
  $scope.rows = 10
  $scope.listings = []
  $scope.getMore = ->
    $http.get("/listings.json?start=#{$scope.start}&rows=#{$scope.rows}&lat=#{$scope.lat}&lon=#{$scope.lon}").success (data) ->
      for entry in data
          $scope.listings.push(entry)
      $scope.start += $scope.rows
  $scope.getMore()