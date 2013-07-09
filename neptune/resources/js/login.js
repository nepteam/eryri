$(document).ready(function () {
    var notifier = new Notifier('NEP Security'),
        $form = $('form');

    $form.submit(function (e) {
        e.preventDefault();

        var u = $form.find('input[name=u]').val(),
            p = $form.find('input[name=p]').val();

        $.ajax({
            url: '/login',
            method: 'post',
            data: {
                u: u,
                p: p
            },
            success: function (user) {
                notifier.notify('Welcome to the party, ' + user.name + '.');
                history.go(0);
            },
            statusCode: {
                400: function () {
                    notifier.notify('Missing username or password');
                },
                403: function () {
                    notifier.notify('Invalid username or password');
                }
            }
        });
    });
});