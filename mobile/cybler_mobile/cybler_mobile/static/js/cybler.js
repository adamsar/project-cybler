  var ListingController, urlParams;

  urlParams = {};

  window.onpopstate = function() {
    var decode, match, p, query, search, _results;
    p = /\+/g;
    search = /([^&=]+)=?([^&]*)/g;
    decode = function(s) {
      return decodeURIComponent(s.replace(pl, " "));
    };
    query = window.location.search.substring(1);
    _results = [];
    while (match = search.exec(query)) {
      _results.push(urlParams[decode(match[1])] = decode(match[2]));
    }
    return _results;
  };

  ListingController = function($scope, $http) {
    $scope.start = 0;
    $scope.rows = 10;
    $scope.listings = [];
    $scope.getMore = function() {
      var baseUrl, key, value;
      baseUrl = "/listings.json?";
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
