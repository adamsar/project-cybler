  var ListingController;

  ListingController = function($scope, $http) {
    $scope.start = 0;
    $scope.rows = 10;
    $scope.listings = [];
    $scope.getMore = function() {
      var baseUrl;
      baseUrl = "/listings.json?start=" + $scope.start + "&rows=" + $scope.rows;
      if ($scope.queryParams) {
        baseUrl += "&" + queryParams;
      }
      return $http.get(baseUrl).success(function(data) {
        var entry, _i, _len;
        for (_i = 0, _len = data.length; _i < _len; _i++) {
          entry = data[_i];
          $scope.listings.push(entry);
        }
        $scope.start += $scope.rows;
      });
    };
    return $scope.getMore();
  };

