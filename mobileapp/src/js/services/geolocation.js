angular.module('App.services.Geolocation', [
  'App.services.DeviceReady'
]).factory('getCurrentPosition', function(deviceReady, $document, $window, $rootScope){
  return function(done, fail) {
    deviceReady(function(){
      try {
          if (navigator.geolocation !== null) {
            navigator.geolocation.getCurrentPosition(function(position){
                done(position);
            }, function(error){
                fail();
                //throw new Error('Unable to retreive position');
            }, {
              timeout: 10000,
              maximumAge: 11000,
              enableHighAccuracy: true
            });
          }else{
            fail();
          }
      } catch (e) {
          fail();
          console.log(e.message);
      }
    });
  };
});
