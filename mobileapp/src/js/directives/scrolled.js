
(function(angular, undefined){
    //'use strict';
    function createDirective(module, attrName){
        module.directive(attrName, function(){
          return function(scope, element, attrs) {
              var page = element[0].querySelector(".ons-page-inner");
              angular.element(page).bind('scroll', function () {
                if (this.scrollTop + this.offsetHeight >= this.scrollHeight) {
                    scope[attrs.scrolled] = true;
                }else{
                    scope[attrs.scrolled] = false;
                }
              });
              scope.$apply();
        };
      });
    }
    var module = angular.module('App.directives.scrolled', []);
    createDirective(module, 'scrolled');
}(angular));
