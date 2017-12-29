var url = '/lights/';

// Start Ready
$(document).ready(function() { 
    
    // prepare the color picker
    $('#color_picker').minicolors(
        {
            control: 'wheel',
            format: 'rgb',
            swatches: ["rgb(255, 0, 0)", "rgb(0, 255, 0)", "rgb(0, 0, 255)", "rgb(255, 255, 255)", "rgb(0, 0, 0)"],
            change: function(value, opacity) {
                //console.log(value + ' - ' + opacity);
                set_color(value);
            }
        }
    );
    
    color_last_value = '';
    function set_color(value) {
        if (color_last_value != value) {
            color_last_value = value;
            $.ajax({
                type: 'POST',
                url: url + 'color/',
                contentType: "application/json; charset=UTF-8",
                data: JSON.stringify($('#color_picker').minicolors('rgbObject')),
                dataType: 'html',
                cache: false,
                success: function(html) {
                    console.log('set color: success');
                    $('#rgb_display').html(color_last_value);
                }
            });
        }
    }

    bottom_to_top_last_value = -1;
    $("#bottom_to_top").rangeslider({
        'update': true,
        'polyfill': false,
        onSlide: function(position, value) {
            if (bottom_to_top_last_value != value) {
                bottom_to_top_last_value = value;
                $.ajax({
                    type: 'POST',
                    url: url + 'slide/bottom/' + value,
                    data: {},
                    dataType: 'html',
                    cache: false,
                    success: function(html) {
                        console.log('slide bottom: success');
                    }
                });
            }
        },
    });
    
    top_to_bottom_last_value = -1;
    $("#top_to_bottom").rangeslider({
        'update': true,
        'polyfill': false,
        onSlide: function(position, value) {
            if (top_to_bottom_last_value != value) {
                top_to_bottom_last_value = value;
                $.ajax({
                    type: 'POST',
                    url: url + 'slide/top/' + value,
                    data: {},
                    dataType: 'html',
                    cache: false,
                    success: function(html) {
                        console.log('slide top: success');
                    }
                });
            }
        },
    });
    
    $("#off").on("click", function(e) {
        $.ajax({
            type: 'POST',
            url: url + 'off/',
            data: {},
            dataType: 'html',
            cache: false,
            success: function(html) {
                console.log('off: success');
            }
        });
    });
    
    $("#on").on("click", function(e) {
        $.ajax({
            type: 'POST',
            url: url + 'on/',
            data: {},
            dataType: 'html',
            cache: false,
            success: function(html) {
                console.log('on: success');
            }
        });
    });

    $("#random_color").on("click", function(e) {
        $.ajax({
            type: 'POST',
            url: url + 'random_color/',
            data: {},
            dataType: 'html',
            cache: false,
            success: function(html) {
                console.log('random_color: success');
                // set this so when the "change" event fires it doesn't post back to the server
                color_last_value = html;
                $('#color_picker').minicolors('value', html);
                $('#rgb_display').html($('#color_picker').minicolors('rgbString'));
            }
        });
    });
    
    $(".btn-pattern").on('click', function(e) {
        pattern = $(this).data("pattern");
        post_url = url + 'pattern' + '?name=' + pattern + '&delay=' + $("#delay").val() + '&pause=' + $("#pause").val();
        $.ajax({
            type: 'POST',
            url: post_url,
            data: {},
            dataType: 'html',
            cache: false,
            success: function(html) {
                console.log('success: ' + post_url);
            }
        });
    });
});
