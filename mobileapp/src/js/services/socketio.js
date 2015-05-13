//socket factory that provides the socket service
angular.module('App.services.Socketio', [
  'btford.socket-io'
])
.factory('socket', function (socketFactory) {
  var myIoSocket = io.connect('http://127.0.0.1:8080/chat');
  var mySocket = socketFactory({
    ioSocket: myIoSocket
  });
  return mySocket;
});
