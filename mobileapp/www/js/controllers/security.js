appCtrlsSecureSecure = angular.module('App.controllers.Security', []).config(function($httpProvider) {
  $httpProvider.interceptors.push('httpResponseErrorInterceptor');
})
.run(['$rootScope', '$injector', function($rootScope,$injector) {
    $injector.get("$http").defaults.transformRequest = function(data, headersGetter) {
        if ($rootScope.oauth) headersGetter()['Authorization'] = 'Bearer ' + $rootScope.oauth.access_token;
        if (data) {
            if(headersGetter()["Content-Type"] == 'application/json' || headersGetter()["Content-Type"] == "application/json;charset=utf-8"){
              return angular.toJson(data);
            }
            return data;
        }
    };
}]);

appCtrlsSecureSecure.factory('httpResponseErrorInterceptor',function($q, $injector, $rootScope, $location, $timeout) {
  return {
    'responseError': function(response) {
      if (response.status === 0) {
        $rootScope.maxRetryCount =  angular.isUndefined($rootScope.maxRetryCount) ? 3 : $rootScope.maxRetryCount;
        $rootScope.retries = angular.isUndefined($rootScope.retries) ? $rootScope.maxRetryCount : $rootScope.retries;
        if($rootScope.retries > 0){
          // should retry
          $rootScope.retries--;
          retryModal.show();
          $timeout(function () {
            var $http = $injector.get('$http');
            return $http(response.config);
          }, 5000);
        }else{
          delete $rootScope.retries;
          retryModal.hide();
          // give up
          ons.notification.alert({title: 'Error: Connection Fail!', message: 'Could not Connect to Server. Please Check your connection!'});
          return $q.reject(response);
        }
      }else{
        retryModal.hide();
      }
      if (response.status===401 && response.data.error && response.data.error === "invalid_token") {
        // should retry
        if ($rootScope.oauth){
			refresh_token = $rootScope.oauth.refresh_token;
			var $http = $injector.get('$http');
			$http({
				method: 'GET',
				url: OAUTH_ACCESS_TOKEN_URl+'?grant_type=refresh_token&refresh_token='+refresh_token+'&client_secret='+clientSecret+'&client_id='+clientId+'&redirect_uri=' + encodeURIComponent(OAUTH_CALLBACK)
			}).success(function(data){
				$rootScope.oauth = data;
				return $http(response.config);
			}).error(function(data){
				if (data.status===401 && data.error && data.error === "invalid_token"){
					$rootScope.oauth = null;
          menu.setMainPage('login.html', {closeMenu: true});
				}
			});
		}else{
			menu.setMainPage('login.html', {closeMenu: true});
		}
      }
      // give up
      return $q.reject(response);
    }
  };
});
