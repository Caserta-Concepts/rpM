var rpmApp = angular.module('rpmApp', []);

rpmApp.controller('IndexCtrl', function ($scope, $http) {
  $scope.results = [];
  $scope.userid = '572';
  $scope.itemid = '7';
  $scope.numitems = '25';

  $scope.item_description = '';

  $scope.hasData = false;

  $scope.lookupItem = function (itemid) {
    var api_url = 'http://127.0.0.1:5000/getItems?callback=JSON_CALLBACK&item_id=';

    if (itemid) {
      if (itemid.charAt(0) != 'I')
        api_url += 'I';
      api_url += itemid;
      $http.jsonp(api_url).success(function (data) {
        $scope.item_description = data[0].name;
      });
    }
  }

  $scope.getRecommendations = function (userid, itemid, numitems) {
    if (!userid) userid = 0;
    if (!itemid) itemid = 0;
    if (!numitems) numitems = 10;

    var api_url = 'http://127.0.0.1:5000/recommenderitems/'
    api_url += userid + '/';
    api_url += itemid + '/';
    api_url += numitems
    api_url += '/detail?callback=JSON_CALLBACK';

    $scope.hasData = false;

    $http.jsonp(api_url).success(function (data) {
      $scope.results = data;
      $scope.hasData = true;
    });
  }
});