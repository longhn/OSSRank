'use strict';

var app = angular.module('ossrank', ['ngRoute', 'ngResource'])
    .config(function ($routeProvider) {
        $routeProvider
            .when('/', {
                templateUrl: 'views/main.html',
                controller: 'HomeCtrl'
            })
            .when('/project/:projectId', {
                templateUrl: 'views/project.html',
                controller: 'ProjectCtrl'
            })
            .otherwise({
                redirectTo: '/'
            });
    });

app.factory('Category', function ($resource) {
    return $resource("/api/categories");
});

app.factory('Project', function ($resource) {
    return $resource("/api/projects/:id");
});