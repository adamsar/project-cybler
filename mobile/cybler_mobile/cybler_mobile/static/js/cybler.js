  var ListingController, getUrlVars, urlParams;

  getUrlVars = function() {
    var hash, hashes, vars, _i, _len;
    vars = [];
    hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
    for (_i = 0, _len = hashes.length; _i < _len; _i++) {
      hash = hashes[_i];
      hash = hash.split("=");
      vars[hash[0]] = hash[1];
    }
    return vars;
  };

  urlParams = getUrlVars();

  ListingController = function($scope, $http) {
    $scope.start = 0;
    $scope.rows = 10;
    $scope.listings = [];
    $scope.getMore = function() {
      var baseUrl, key, value;
      baseUrl = "/listings.json?start=" + $scope.start + "&rows=" + $scope.rows;
      for (key in urlParams) {
        value = urlParams[key];
        baseUrl += "&" + key + "=" + value;
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
