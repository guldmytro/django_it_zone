'use strict';

(function initBrands() {
    let path = location.pathname.split('/');
    if (path.length === 4) {
        let queryStr = path[2];
        let queryArr = queryStr.split(';');
        const queryDict = {};
        for (const item of queryArr) {
            const itemArr = item.split(':');
            if (itemArr.length === 2) {
                queryDict[itemArr[0]] = itemArr[1];
            }
        }
        if ('letter' in queryDict) {
            $(`[name="brand-start"][value="${queryDict['letter']}"]`).prop('checked', true);
        }
        if (queryDict['filter'] === 'top') {
            $(`[name="brand-type"][value="${queryDict['filter']}"]`).prop('checked', true);
        }
    }
})();
let page = 1;
$('[name="brand-start"], [name="brand-type"]').change(function() {
    
    if ($(this).attr('name') === 'brand-start') {
        $('[name="brand-type"]:checked').prop('checked', false);
    } else {
        $('[name="brand-start"]:checked').prop('checked', false);
    }
    page = 1;
    sendBrandQuery();
});
$('.brands').on('click', '.pagination button', function() {
    page = $(this).attr('data-page');
    sendBrandQuery();
});

function parseQueryString() {
    let result = `page:${page};`;
    const letter = $('[name="brand-start"]:checked').val();
    const filter = $('[name="brand-type"]:checked').val();
    if (letter) {
        result += `letter:${letter.toLowerCase()}`;
    }
    if (filter) {
        result += `filter:${filter.toLowerCase()}`;
    }
    return result;
}

function parseQueryUrl() {
    const queryData = parseQueryString();
    let path = location.pathname.split('/producers/');
    path = path[0] + '/producers/';
    path = path.replace('//', '/');
    return location.protocol + '//' + location.host + path + queryData + '/';
}

function sendBrandQuery() {
    let newUrl = parseQueryUrl();
    window.history.pushState(null, null, newUrl);
    $('.brands-filters, .brands-group').addClass('loading');
    $.ajax({
        url: newUrl,
        method: 'get',
        contentType: 'application/json; charset=utf-8',
        success: function(response) {
            $('.brands-filters, .brands-group').removeClass('loading');
            const res = $(response).find('.brands-group a, .brands-group > p, .pagination');
            $('.brands-group').html(res);
        }
    });
}

