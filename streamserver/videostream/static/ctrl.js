$(function() {
    var show_image = function(){
        $.getJSON('/videostream/get_image', { }, function(data) {
            $('#img').html('<img src="data:image/png;base64,' + data.base64img + '" />');
            show_image();
        });
    }

    show_image();

    keys = ['w', 's', 'd', 'a', 'n', '1', '2', '3', '4', '5']
    $(document).on('keypress', function(e) {
        if (keys.includes(e.key)){
            data = JSON.stringify({'key':e.key});
            $.post('/videostream/key', data, function(response) {
            }, 'json');
        }
    });

});
