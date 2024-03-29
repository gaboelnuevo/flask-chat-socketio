angular.module('App.services.DeviceReady', [])
.factory('deviceReady', function(){
  return function(done) {
    if (typeof window.cordova === 'object') {
      document.addEventListener('deviceready', function () {
        done();
      }, false);
    } else {
        angular.element(document).ready(function () {
            done();
        });
    }
  };
});
