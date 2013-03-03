$(function() {
    $('#price_table').fixheadertable({ 
        wrapper: false,
        zebra: true,
        resizeCol: true,
        height: 390,
        colratio: [215, 145, 110, 90],
    });
    $('.filter').change(function() {
        $('.priceline').hide();
        $('.priceline:first').fadeOut('slow', function() {
            var markers = '';
            $('.filter').each(function() {
                var marker = $(this).val();
                if (marker !== 'all')
                    markers += '.marker_' + marker;
            });
            $('.priceline' + markers).show();
        });
    });
});
