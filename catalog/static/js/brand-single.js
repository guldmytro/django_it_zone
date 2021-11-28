$('.brand').on('click', '.pagination a', function(e) {
    e.preventDefault();
    const url = $(this).attr('href');
    sendPaginationQuery(url);
});

function sendPaginationQuery(url) {

    window.history.pushState(null, null, url);
    $('.brands-filters, .brands-group').addClass('loading');
    $.ajax({
        url: url,
        method: 'get',
        contentType: 'application/json; charset=utf-8',
        success: function(response) {
            const res = $(response).find('.archive-product, .pagination');
            $('.wishlist-group').html(res);
            document.querySelector('.wishlist-group').scrollIntoView({
                behavior: 'smooth'
            });
        }
    });
}