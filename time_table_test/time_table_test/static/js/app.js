/// <reference path="./angular.min.js" />

let app =
	angular
	.module("App", [])
	.controller("tableController", ($scope, $http) => {
		$scope.faculties = [];
		$http.get("../data/data.json")
			.then((response) => {
				$scope.faculties = response.data.faculties;
			}, (err) => {

			});

		$scope.SortColumn = function (column) {
			$scope.ColumnName = column;
			$scope.SortBy = ($scope.ColumnName == column) ? !$scope.SortBy : false;
		}

		$scope.getSortClass = function (column) {
			if ($scope.ColumnName == column) {
				return $scope.SortBy ? 'mouse-down' : 'mouse-up';
			}
			return '';
		}

	})
	.controller("intialInputs",($scope) =>{

		$scope.noOfClass = 0;
		
		$scope.range = function (min, max, step) {
			step = step || 1;
			var input = [];
			for (var i = min; i <= max; i += step) input.push(i);
			return input;
		};

	});