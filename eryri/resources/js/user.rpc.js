UserRpcService = function (rpcUrl) {
    this.rpcUrl = rpcUrl;
};

UserRpcService.prototype.query = function (query, successCallback) {
    $.ajax({
        url: this.rpcUrl,
        data: {
            query: query
        },
        success: function (response) {
            successCallback(response.users);
        }
    });
};

UserRpcService.prototype.get = function (uid, successCallback) {
    $.ajax({
        url: this.rpcUrl,
        data: {
            uid: uid
        },
        success: function (response) {
            successCallback(response.user);
        }
    });
};