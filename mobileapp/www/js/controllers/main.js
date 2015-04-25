
appCtrlsMain = angular.module('App.controllers.Main', []);

appCtrlsMain.controller('MainController', function($scope, $rootScope){
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
  }
});

appCtrlsMain.controller('ChatListController', function($scope,$rootScope, $timeout, ChatList){
  $scope.scanning = true;
  $scope.childLoad = null;
  $timeout(callAtTimeout, 4000);

  $scope.init = function () {
    ChatList.get({}, function(data) {
      $scope.chats = data.result;
    });
  };

  $scope.getMessages = function(id){
    $scope.chat_id = id;
    myNavigator.pushPage('detail.html', { animation : 'slide' } );
  };

  function callAtTimeout() {
    $scope.scanning = false;
  }

});

appCtrlsMain.controller('ChatController', function($scope,$timeout,$interval,$location,$anchorScroll, Me, MessageList, Message){
  $scope.glued = false;
  $scope.init = function () {
    $scope.messages = [];
    $scope.chat_id = $scope.$parent.chat_id;
    $timeout(load, 1000);
  };

  $scope.load_olds = function($done) {
      $timeout(function() {
        if($scope.messages.length >= 1){
          var first_id = $scope.messages[0].id;
          MessageList.get({chat_id: $scope.chat_id, before_id: first_id, limit: 5}, function(data){
            console.log(data);
            $scope.messages.unshift.apply($scope.messages, data.messages);
          });
        }
        $done();
      }, 1000);
  };

  $scope.getMessages = function(){
    $scope.messages = [];
    MessageList.get({chat_id: $scope.chat_id, limit: 20}, function(data){
      $scope.messages = data.messages;
    });
  };

  $scope.PostMsg = function(){
    if (!$scope.posting && $scope.msgbody != "" && angular.isDefined($scope.chat_id)){
      $scope.posting = true;
      var msg = new Message;
      msg.body = $scope.msgbody;
      $scope.msgbody = "";
      msg.$save({chat_id : $scope.chat_id}, function(data){
        $scope.scrollTo();
        $scope.reset();
        $scope.posting = false;
        fetch_new_msg();
      });
    }else{
      $scope.posting = false;
    }
  };

  $scope.scrollTo = function() {
    $scope.glued = true;
    $timeout(function(){
      $scope.glued = false;
    }, 2000);
  };

  function fetch_new_msg(){
    if (angular.isDefined($scope.chat_id)){
      if($scope.messages.length >= 1){
        last_id = $scope.messages[($scope.messages.length -1)].id;
        MessageList.get({chat_id: $scope.chat_id, after_id: last_id}, function(data){
          angular.forEach(data.messages, function(msg,index) {
            $scope.glued = $scope.scrolled;
            $timeout(function(){
              $scope.glued = false;
            }, 2000);
            $scope.messages.push(msg);
            //$anchorScroll();
          });
        });
      }else{
        $scope.getMessages();
      }
    }
  };

  function load(){
    Me.get({}, function(data){
      $scope.me = data;
    });
    $scope.getMessages();
    $scope.intervalPromise = $interval(fetch_new_msg,3000, false);
    $scope.$on('$destroy',function(){
    if($scope.intervalPromise)
          $interval.cancel($scope.intervalPromise);
    });
  };

  $scope.reset = function() {
    $scope.msgbody = "";
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
