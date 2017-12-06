// $.getScript("https://cdnjs.cloudflare.com/ajax/libs/angular.js/1.6.5/angular.min.js", function () {

let app =
  angular
    .module('mainPage', [])
    .config(function($httpProvider){
      $httpProvider.defaults.xsrfCookieName='csrftoken';
      $httpProvider.defaults.xsrfHeaderName='X-CSRFToken';
    })
    // .config(function ($routeProvider) {
    //   $routeProvider
    //     .when('/', {
    //       templateUrl: './components/home.html',
    //       controller: 'homePageController'
    //     })
    //     .when('/dashboard', {
    //       templateUrl: './components/dashboard.html',
    //       controller: 'dashboardPageController'
    //     })
    //     .when('/timetable', {
    //       templateUrl: './components/timetable.html',
    //       controller: 'timetablePageController'
    //     })
    //     .otherwise({
    //       templateUrl: '404.html'
    //     })
    // })

    .controller("homePageController", function ($scope, $location) {
      $scope.goDashboard = () => {
        $location.path('/dashboard');
      }
      $scope.goTimetable = () => {
        $location.path('/timetable');
      }
    })

    .controller("dashboardPageController", function ($scope, $http) {

      $scope.initialize = () => {
        $('.modal').modal();
        $('.collapsible').collapsible();
        $('.tap-target').tapTarget('open');
        setTimeout(() => {
          $('select').material_select();
          $('.tooltipped').tooltip({
            delay: 50
          });
        }, 1000);
      };


      $scope.CheckData = () => {
        $http({
          method: 'GET',
          url: 'fetch_data'
        }).then((res) => {          
          $scope.classes = res.data.classes;
          $scope.hasClasses = true;
        }, (err) => {
          console.log('Something Wrong for fetching data');
        });
      };

      $scope.classes = {};
      $scope.hasClasses = false;
      // $http.get('./data/d.json')
      //     .then((res) => {
      //         $scope.classes = res.data;
      //         $scope.hasClasses = true;
      //     }, (err) => {
      //         console.log('Something Wrong');
      //     });

      $scope.subjectFaculties = [];
      $scope.classIndex = 0;
      $scope.subIndex = 0;
      $scope.getFaculties = (cIndex, subIndex, subject) => {
        $scope.classIndex = cIndex;
        $scope.subIndex = subIndex;

        $scope.subjectFaculties = subject.faculties;
        $scope.subjectLoad = subject.sub_load;
      };
      $scope.newFac = {};
      $scope.addNewFaculty = () => {
        $scope.classes[$scope.classIndex].subjects[$scope.subIndex].faculties.push({
          "name": $scope.newFac.name,
          "work_load": $scope.newFac.load
        });
        $scope.newFac = {};
      };
      $scope.CreateNewClass = () => {
      // add_semster

        var NewClass = $scope.NewClassName;

        // $http.defaults.headers.post["Content-Type"]="application/x-www-form-urlencoded"
        //$http.defaults.headers.post["Content-Type"]="application/json"

        var d = $.param({ class_name : NewClass });
        $http({
          method: 'POST',
          url: 'add_semester',
          data: {
            class_name: NewClass
          },
          // data: d,
          // data: 'class_name=' + NewClass,
          headers: {'Content-Type': 'application/x-www-form-urlencoded;Charset=utf-8;'}
          // data: $.param($scope.NewClassName),
        }).then((res) => {
          if(res.data.status == "success" ){
            $scope.classes.push({
              "name": NewClass,
              "subjects": []
             });
            }
        }, (err) => {
          console.log('Something Wrong for in creating new class');
        });

        $scope.NewClassName = '';

      };
      $scope.newSub = {};
      $scope.newSub_Class = (cIndex) => {
        $scope.classIndex = cIndex;
      };
      $scope.addNewSubject = () => {
        $scope.classes[$scope.classIndex].subjects.push({
          "name": $scope.newSub.Sub_Name,
          "sub_code": $scope.newSub.Sub_Code,
          "sub_load": $scope.newSub.Sub_Load,
          "sub_lec": $scope.newSub.Sub_n_lec,
          "sub_lab": $scope.newSub.Sub_n_lab,
          "sub_tut": $scope.newSub.Sub_n_tut,
          "faculties": []
        });
        $scope.newSub = {};
        $scope.isLecture = false;
        $scope.isLAB = false;
        $scope.isTutorial = false;
      };
    })
    .controller("timetablePageController", function ($scope,$http) {

      $scope.initialize = () => {
        $('select').material_select();
      };

      $scope.getData = () => {
        $http({
          method: 'GET',
          url: 'get_timetable'
        }).then((res) => {     
        console.log(res)     ;
          // $scope.classes = res.data.classes;
          // $scope.hasClasses = true;
        }, (err) => {
          console.log('Something Wrong for fetching data');
        });
      };
    });
// });