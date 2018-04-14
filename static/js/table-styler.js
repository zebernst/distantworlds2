$(document).ready(function() {
    var tRows = $('tr');
    
    // $('table-target').click(function() {
    //     $(this).addClass('table-selected') {

    //     }
    // });

    $(tRows).hover(
        function() {
            $(this).addClass('dw-anim-highlight');
        },
        function() {
            $(this).removeClass('dw-anim-highlight');
    });    
}); 