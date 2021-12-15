(function() {
'use strict';

$('.variation-filter__header').on('click', function() {
    const $this = $(this);
    $this.toggleClass('active');
    $this.next('.variation-fields').find('.variation-fields__fieldset').slideToggle(200);
});

$('.btn_filter').on('click', function(e) {
    e.preventDefault();
    $('form.variation-filters').slideToggle(200);
});

$('.variation-tabs button').on('click', function(e) {
    e.preventDefault();
    const $this = $(this);
    if ($this.hasClass('active')) {
        return false;
    }
    const id = $this.attr('data-id');
    const tab = $(`#${id}`);
    if (tab.length === 1) {
        $('.variation-tabs button.active').removeClass('active');
        $('.variation-content-group__item.active').removeClass('active');
        $this.addClass('active');
        tab.addClass('active');
    }
});

// variation goTo anchor
$('.btn_goto-vars').on('click', function(e) {
    const headerHeight = $('.header').outerHeight();
    console.log(headerHeight);
    $('html, body').animate({scrollTop: $('.variation-section').offset().top - headerHeight - 10},'slow');
});

// filtering
(function initFilters() {
    let path = location.pathname.split('/');
    if (path.length === 5) {
        params = path[3].split(';');
        for (const p of params) {
            const pArray = p.split(':');
            const key = pArray[0];
            const vals = pArray[1].split('=');
            if (key === 'price') {
                $(`[name='price']`).attr('data-to', vals[1]).attr('data-from', vals[0]);
            } else if (key === 'order') {
                $('#product-order').val(vals[0]);
            } else {
                for (let val of vals) {
                    $(`[name='${key}'][value='${decodeURI(val)}']`).prop('checked', true);
                }
            }

        }
    }
    const htmlToPaste = $('#v-1 > *');
    if (!htmlToPaste.length) {
        $('#v-1').html('<p>По Вашему запросу товаров не найдено.</p>');
    }
})();

const filterForm = $('form.variation-filters');
let filterTimer = false;

filterForm.find('input').on('change', function() {
    if (filterTimer) {
        clearTimeout(filterTimer);
    }
    filterTimer = setTimeout(() => {
        filterForm.submit();
    }, 800);
});

filterForm.find('[type="reset"]').on('click', function() {
    if (filterTimer) {
        clearTimeout(filterTimer);
    }
    filterTimer = setTimeout(() => {
        filterForm.submit();
    }, 800);
});

filterForm.submit(function(e) {
    e.preventDefault();
    const $this = $(this);
    const newUrl = getFilteredUrl($this);
    $('.catalog-results').slideUp(100);
    $('.sidebar_search input').val('');
    window.history.pushState(null, null, newUrl);
    $('.variation-section').addClass('loading');
    $.ajax({
        url: newUrl,
        method: 'get',
        contentType: 'application/json; charset=utf-8',
        success: function(response) {
            const htmlToPaste = $(response).find('#v-1 > *');
            if (htmlToPaste.length) {
                $('#v-1').html(htmlToPaste);
            } else {
                $('#v-1').html('<p>По Вашему запросу товаров не найдено.</p>');
            }
            $('.variation-section').removeClass('loading');
        }
    });
});

function getFilteredUrl(form) {
    const queryData = getQueryData();
    let path = location.pathname.split('/');
    if (path.length === 5) {
        path.pop();
        path.pop();
    }
    path = path.join('/');
    path += '/';
    path = path.replace('//', '/');
    if (queryData.length) {
        return location.protocol + '//' + location.host + path + queryData + '/';
    } else {
        return location.protocol + '//' + location.host + path;
    }
    
}

function getQueryData() {
    const filters = {};
    let strArr = [];
    
    filterForm.find('input:checked').each(function() {
        const $this = $(this);
        const key = $this.attr('name');
        const value = $this.val();
        if (!filters[key]) {
            filters[key] = [];
        }
        filters[key].push(value);
    });
    for (const filter in filters) {
        const params = filters[filter].join('=');
        strArr.push(`${filter}:${params}`);
    }
    let result = strArr.join(';');
    return result;
}

})();