// A adaptation of emojify

(function(angular, undefined){
    //'use strict';

    function createDirective(module, attrName, emoticons, emojinames){
        module.directive(attrName, ['$parse', '$window', function($parse, $window){
            return {
                priority: 1,
                restrict: 'A',
                link: function(scope, $el, attrs){
                    var el = $el[0];
                    twemojify.run(el);
                    scope.content = el.innerHTML ;
                    scope.$watch('content', function() {twemojify.run(el);});
                }
            };
        }]);
    }
    var module = angular.module('App.directives.emojifymsg', []);

    createDirective(module, 'emojifyMessage');
}(angular));
