/*function convertUTCDateToLocalDate(date) {
    var newDate = new Date(date.getTime()+date.getTimezoneOffset()*60*1000);

    var offset = date.getTimezoneOffset() / 60;
    var hours = date.getHours();

    newDate.setHours(hours - offset);

    return newDate;
}*/
var module = angular.module('App.filters.asdate', []);
module.filter("asDate", function () {
    return function (input) {
        return new Date(input);
    }
});
