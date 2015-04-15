var API_HOST = "http://10.0.2.2:5000";
var OAUTH_ACCESS_TOKEN_URl = API_HOST + '/oauth/token';
var OAUTH_ATHORIZE_URL = API_HOST + '/oauth/authorize'
var API_URL = API_HOST + '/api';
var API_BASE = API_URL + '/v1';
var OAUTH_CALLBACK = API_HOST + '/oauth/fakecallback'
var clientId = "2adY5iIDCOr47APLxmPifkgfzDL8CbLzLgBeUpgJ";
var clientSecret = "gfNzhsdGMx41yFq8Vh79oHZYCYyPlF0k3rjNribHeP7BEUgXhl";

(function(){
	//ons.bootstrap();
	angular.module('App', [
		'ngResource',
		'ngAnimate',
		'onsen',
		'App.directives.scrollGlue',
		'App.services.Resources',
		'App.controllers.Login',
		'App.controllers.Main',
		'App.controllers.Security']);
})();
