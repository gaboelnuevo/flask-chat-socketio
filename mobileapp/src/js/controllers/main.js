
var appCtrlsMain = angular.module('App.controllers.Main', ['App.services.DeviceReady']);

appCtrlsMain.controller('MainController', function($scope, $rootScope, deviceReady){
  $rootScope.$on('userLogIn', function () {
    $scope.logged = true;
  });
  $rootScope.$on('userLogOff', function () {
    $scope.logged = false;
  });
  $scope.dialogs = {};
  $scope.showDialog = function(dlg) {
    if (!$scope.dialogs[dlg]) {
      ons.createDialog(dlg).then(function(dialog) {
        $scope.dialogs[dlg] = dialog;
        dialog.show();
      });
    }
    else {
      $scope.dialogs[dlg].show();
    }
  };
  $scope.logged = ($rootScope.oauth  !== undefined) && ($rootScope.oauth  !== null);
  deviceReady(function(){
    if(!$scope.logged){
        menu.setMainPage('login.html', {closeMenu: true});
    }
  });
});

appCtrlsMain.controller('NewChatController', function($scope, $rootScope, getCurrentPosition, Chat){
    $scope.newChat = function(){
    var chat = new Chat();
    getCurrentPosition(function(position){
        chat.name = $scope.chatname;
        chat.latitude  = position.coords.latitude;
        chat.longitude = position.coords.longitude;
        chat.$save({}, function(data){
            $rootScope.$broadcast('newChatCreated');
        });
    },function(){
        ons.notification.alert({message: 'Error al obtener position geografica!'});
    });
    dialog.hide();
  };
});

appCtrlsMain.controller('GeoCtrl', function($scope,getCurrentPosition) {
    getCurrentPosition(function(position){
      $scope.lat  = position.coords.latitude;
      $scope.lon = position.coords.longitude;
    },function(){
        ons.notification.alert({message: 'Error al obtener position geografica!'});
    });
});


appCtrlsMain.controller('ChatListController', function($scope,$rootScope, $timeout, ChatList, getCurrentPosition){
  $scope.scanning = false;
  $scope.childLoad = null;

  $scope.init = function () {
    $scope.discovery();
  };

  $rootScope.$on('newChatCreated', function () {
    $scope.discovery();
  });

  $scope.discovery = function() {
    $scope.scanning = true;
    $timeout(callAtTimeout, 4000);
    getCurrentPosition(function(position){
      ChatList.get({
          latitude: position.coords.latitude,
          longitude: position.coords.longitude},
        function(data) {
          $scope.chats = data.result;
        });
    },function(){
        ons.notification.alert({message: 'Error: Unable to retreive position!'});
    });
  };

  $scope.getMessages = function(id){
    $scope.chat_id = id;
    myNavigator.pushPage('detail.html', { animation : 'slide' });
  };

  function callAtTimeout() {
    $scope.scanning = false;
  }
});

appCtrlsMain.controller('ChatController', function($scope, $rootScope,$timeout,$interval, Me, MessageList, Message,Socket){
  $scope.glued = false;
  $scope.fetching = false;
  $scope.msgbody = "";
  $scope.messages = [];
  //$scope.intervalPromise = $interval(fetch_new_msg,3000, false);
  $scope.$on('$destroy',function(){
  if($scope.intervalPromise)
    $interval.cancel($scope.intervalPromise);
  });

  $scope.init = function () {
    $scope.chat_id = $scope.$parent.chat_id;
    $timeout(load, 1000);
  };

  Socket.on('event connected', function(data) {
      if ($rootScope.oauth)
        Socket.emit('authenticate', {'token': $rootScope.oauth.access_token});
  });


  $rootScope.$watch('oauth', function(newVal, oldVal) {
    if ($rootScope.oauth)
        Socket.emit('authenticate', {'token': $rootScope.oauth.access_token});
  });

  Socket.on('authenticated', function(data) {
      console.log(data.msg);
      Socket.emit('joined', {'room': $scope.chat_id.toString()});
  });

  Socket.on('authentication failed', function(data) {
      console.log(data.msg);
  });

  Socket.on('status', function(data) {
      console.log(data.msg);
  });

  Socket.on('message', function(data) {
      console.log(data.msg);
      $scope.messages.push(data.msg);
      if($scope.scrolled){
          $scope.scrollTo();
      }
  });

  $scope.load_olds = function($done) {
      $timeout(function() {
        if($scope.messages.length >= 1){
          var first_id = $scope.messages[0].id;
          MessageList.get({chat_id: $scope.chat_id, before_id: first_id, limit: 5}, function(data){
            $scope.messages.unshift.apply($scope.messages, data.messages);
          });
        }
        $done();
      }, 1000);
  };

  $scope.getMessages = function(){
    $scope.messages = [];
    MessageList.get({chat_id: $scope.chat_id, limit: 10}, function(data){
      $scope.messages = data.messages;
      $scope.scrollTo();
      $scope.scrolled = true;
    });
  };

  $scope.PostMsg = function(){
    if (!$scope.posting && $scope.msgbody !== "" && angular.isDefined($scope.chat_id)){
      $scope.posting = true;
      var msg = new Message();
      msg.body = $scope.msgbody;
      $scope.msgbody = "";
      msg.$save({chat_id : $scope.chat_id}, function(data){
        $scope.reset();
        fetch_new_msg();
        $scope.scrollTo();
        $scope.posting = false;
      });
    }
  };

  $scope.scrollTo = function() {
    $scope.glued = true;
    var scrollPromise = $timeout(function(){
      $scope.glued = false;
    }, 2000);
    $scope.$on('$destroy', function(){
        $timeout.cancel(scrollPromise);
    });
  };

  function fetch_new_msg(){
    if($scope.fetching === false){
        $scope.fetching = true;
        if (angular.isDefined($scope.chat_id)){
          if($scope.messages.length >= 1){
            var last_id = $scope.messages[($scope.messages.length -1)].id;
            MessageList.get({chat_id: $scope.chat_id, after_id: last_id}, function(data){
              angular.forEach(data.messages, function(msg,index) {
                if($scope.scrolled){
                    $scope.scrollTo();
                }
                $scope.messages.push(msg);
              });
            });
          }else{
            $scope.getMessages();
            $scope.fetching = false;
          }
        }
        $scope.fetching = false;
    }
  }

  function load(){
    Me.get({}, function(data){
      $scope.me = data;
      $scope.getMessages();
    });
  }

  $scope.reset = function() {
    $scope.msgbody = "";
  };
});

appCtrlsMain.controller('ChatIOController', function($scope,$timeout,$interval, socket){
  $scope.glued = false;
  $scope.messages = [];

  $scope.$on('socket:error', function (ev, data) {
    alert(data);
  });

  socket.on('connect', function () {
    socket.emit('joined', {});
  });

  socket.on('message', function(data) {
    $scope.messages.push(data.msg);
    alert(data.msg);
  });

  $scope.init = function(){
    alert("conecting..");
  };
});


appCtrlsMain.controller('RadarController', function($scope){
  // inner variables
  var canvas, ctx;
  var clockRadius = 80;
  var clockImage;

  // draw functions :
  function clear() { // clear canvas function
    ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
  }

  function drawScene() { // main drawScene function
    clear(); // clear canvas
    // get current time
    var date = new Date();
    var seconds = date.getSeconds();
    // save current context
    ctx.save();

    // draw clock image (as background)
    ctx.drawImage(clockImage, 0, 0, 140,140);

    ctx.translate(canvas.width / 2, canvas.height / 2);
    ctx.beginPath();

    ctx.save();
    var theta = (seconds - 15) * 2 * Math.PI / 45;
    ctx.rotate(theta);
    ctx.beginPath();
    ctx.moveTo(0, 0);
    ctx.lineTo(0, 3);
    ctx.lineTo(clockRadius * 0.9, 1);
    ctx.lineTo(clockRadius * 0.9, -1);
    ctx.fillStyle = '#808080';
    ctx.fill();
    ctx.restore();

    ctx.restore();
  }

  // in controller
  $scope.init = function () {
    canvas = document.getElementById('canvas');
    ctx = canvas.getContext('2d');

    // var width = canvas.width;
    // var height = canvas.height;

    clockImage = new Image();
    clockImage.src = 'images/radar.png';

    setInterval(drawScene, 1000); // loop drawScene
  };
});

appCtrlsMain.controller('SettingsController', function($scope, Me){
    Me.get({}, function(data){
      $scope.me = data;
    });
});

appCtrlsMain.controller('ProfileController', function($scope, Me){
    Me.get({}, function(data){
      $scope.user = data;
    });
});
