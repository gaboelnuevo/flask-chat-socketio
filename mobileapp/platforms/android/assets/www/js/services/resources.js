appResources = angular.module('App.services.Resources', []);

appResources.factory('Chat', function($resource) {
  return $resource(API_BASE + '/chats/:id'); // Note the full endpoint address
});

appResources.factory('ChatList', function($resource) {
  return $resource(API_BASE + '/chats'); // Note the full endpoint address
});

appResources.factory('MessageList', function($resource) {
  return $resource(API_BASE + '/chats/:chat_id/messages'); // Note the full endpoint address
});

appResources.factory('Message', function($resource) {
  return $resource(API_BASE + '/chats/:chat_id/messages/:id'); // Note the full endpoint address
});

appResources.factory('Me', function($resource) {
  return $resource(API_BASE + '/me'); // Note the full endpoint address
});
