var streamApp = angular.module('streamerApp', ['ngResource']);
streamApp.controller('StreamerController', function($scope, $http) {
    var loadData = function() {
        $http.get('api/streams').
            success(function(data) {
                $scope.streams = data.streams;    
            });
    }
    loadData();
    $scope.addChannel = function() {
        $scope.channel.process_status = 'started';
        $http.post('api/streams', {channel: $scope.channel}).
            success(function(data) {
                $scope.streams.push(data.stream);
                $scope.channel = '';
            });
    };
    $scope.remove = function(stream) {
        if ($scope.streams.indexOf(stream) !== -1) {
            $http.delete('api/streams/' + stream.channel).
                success(function(data) {
                    $scope.streams.splice($scope.streams.indexOf(stream), 1);
                });
        }
    }
    $scope.stop = function(stream) {
        $http.put('api/streams/' + stream.channel, {process_status: 'stopped'}).
            success(function(data) {
                stream['process_status'] = data.stream['process_status'];
                stream['channel_status'] = data.stream['channel_status'];
            });
    }
    $scope.start = function(stream) {
        $http.put('api/streams/' + stream.channel, {process_status: 'started'}).
            success(function(data) {
                stream['process_status'] = data.stream['process_status'];
                stream['channel_status'] = data.stream['channel_status'];
            });
    }
});
