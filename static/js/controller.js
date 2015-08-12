var rest_controller = angular.module('rest_app', []).config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

rest_controller.controller('rest-controller', function ($scope, $http) {
    $scope.graph = new Chart(STEP, NUM_OF_STEPS)
    $scope.getInterconnections = function() {
        $http.get('/bigquery/interconnections/').success(function(data) {
            $scope.interconnectList = data;
        })
    }

    $scope.getUnitIds = function(name) {
        $http.get('/bigquery/units/?interconnection='+name.slice(1, name.length)).success(function(data) {
            $scope.unitIds = data;
        })
    }

    $scope.getMeasurement = function(inter, unitId) {
        $scope.graph.addRow(inter.slice(1, inter.length), unitId.slice(7,unitId.length));
    }

    $scope.graph.init();

    $scope.getInterconnections()
})