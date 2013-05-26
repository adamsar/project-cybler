  var ListingController, getListings;

  getListings = function(start, rows, lat, lon) {};

  ListingController = function($scope, $http) {
    $scope.start = 0;
    $scope.rows = 10;
    $scope.listings = [];
    $scope.getMore = function() {
      return $http.get("/listings.json?start=" + $scope.start + "&rows=" + $scope.rows + "&lat=" + $scope.lat + "&lon=" + $scope.lon).success(function(data) {
        var entry, _i, _len;
        for (_i = 0, _len = data.length; _i < _len; _i++) {
          entry = data[_i];
          $scope.listings.push(entry);
        }
        return $scope.start += $scope.rows;
      });
    };
    return $scope.getMore();
  };
