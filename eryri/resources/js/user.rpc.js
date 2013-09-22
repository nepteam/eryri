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
            if (response.rid !== self.expectedResponseId) {
                return;
            }

            successCallback(response);
        }
    });
};

UserRpcService.prototype.get = function (uid, successCallback) {
    $.ajax({
        url: this.rpcUrl + uid,
        success: function (response) {
            successCallback(response.user);
        }
    });
};

UserRpcService.prototype.put = function (uid, data, successCallback) {
    $.ajax({
        url: this.rpcUrl + uid,
        data: data,
        method: 'put',
        success: function (response) {
            successCallback(response.user);
        }
    });
};