appCtrlsLogin = angular.module('App.controllers.Login', []);
appCtrlsLogin.controller('LoginController', function($rootScope, $scope, $http, $location){
  $scope.rememberMe = true;
  if ($rootScope.oauth){
    menu.setMainPage('home.html', {closeMenu: true});
  }
  $scope.login = function() {
    $http({
      method: 'POST',
      url: OAUTH_ATHORIZE_URL,
      headers: {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'},
      data: 'redirect_uri='+OAUTH_CALLBACK +'&response_type=code&client_id='+clientId+'&scope=email&username='+this.username+'&password=' + this.password
    }).success(function(data){
      requestToken = data.code;
      $http({
        method: 'GET',
        url: OAUTH_ACCESS_TOKEN_URl + '?grant_type=authorization_code&code='+requestToken+'&client_secret='+clientSecret+'&client_id='+clientId+'&redirect_uri='+ encodeURIComponent(OAUTH_CALLBACK)
      }).success(function(data){
        $rootScope.oauth = data;
        menu.setMainPage('home.html', {closeMenu: true})
      }).error(function(){
        ons.notification.alert({message: 'Something was wrong... Try again!'});
      });
    }).error(function(data){
      if(data){
        if (data.hasOwnProperty('error')) {
          if (data.error === 'incorrect_user_or_password') {
            ons.notification.alert({message: 'Incorrect user or password!'});
          }else{
            ons.notification.alert({message: 'Opps Something is bad!'});
          }
        }else{
          ons.notification.alert({message: 'Opps! Something is bad... check your conection'});
        }
      }else{
        //ons.notification.alert({message: 'Check your connection!'});
      }
    });
  };
});
