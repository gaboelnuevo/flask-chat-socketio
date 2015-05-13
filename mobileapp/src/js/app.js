var API_HOST = "http://127.0.0.1:8080";
//var API_HOST = "http://10.0.2.2:5000";
//var API_HOST = "https://airchat-gtests.rhcloud.com";
var OAUTH_ACCESS_TOKEN_URl = API_HOST + '/oauth/token';
var OAUTH_ATHORIZE_URL = API_HOST + '/oauth/authorize';
var API_URL = API_HOST + '/api';
var API_BASE = API_URL + '/v1';
var OAUTH_CALLBACK = API_HOST + '/oauth/fakecallback';
//var clientId = "BI7pHyGfKVIpZTWPw14bwwn3vyDOpDU2jhbkX440";
//var clientSecret = "b8nDWDPuh3Otk8qDFFWxxu6cCXkjy4DGV0K8REKGLB9V7hai2g";

var clientId = "CMxKbszpmngIPa7Ykph9vxRZdGrqj66IVOKs5EJL";
var clientSecret = "S2j2H3UWBqmMv5ZmKnWHmML5mKZkoDmSntlyMV6NFvSL7XAdlG";

(function(){
	//ons.bootstrap();
	angular.module('App', [
		'ngResource',
		'onsen',
    'ngAnimate',
		'angularMoment',
		'btford.socket-io',
		'App.directives.scrollGlue',
		'App.directives.scrolled',
		'App.directives.emojifymsg',
		'App.filters.asdate',
		'App.services.Resources',
    'App.services.DeviceReady',
    'App.services.Geolocation',
		'App.services.Socketio',
		'App.controllers.Login',
		'App.controllers.Main',
    'App.controllers.Security']);
})();
twemojify.setConfig({
	size : 'twa-lg' // You can change emoji sizes via twa-lg, twa-2x, twa-3x, twa-4x and twa-5x.
});
