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
})();

// range slider
$(".js-range-slider").ionRangeSlider({
    type: 'double',
    postfix: ' ₽'
});

// slideToggle filter
$('.sidebar-filters__header').click(function() {
    const $this = $(this);
    $this.toggleClass('active').next('.sidebar-filters__items').slideToggle(200);
});

// unlock submit btn
let smooth = false;
let filterTimer = false;
const filterForm = $('.form-filters');
const filterFormSubmit = filterForm.find('[type="submit"]');
filterFormSubmit.hide();
filterForm.find('input').on('change', function() {
    setPage();
    if (filterFormSubmit.is(':disabled')) {
        filterFormSubmit.prop('disabled', false);
        if (filterTimer) {
            clearTimeout(filterTimer);
        }
        filterTimer = setTimeout(() => {
            filterForm.submit();
        }, 800);
    }
});

filterForm.submit(function(e) {
    e.preventDefault();
    const $this = $(this);
    filterFormSubmit.prop('disabled', true).text('Загрузка...');
    const newUrl = getFilteredUrl($this);
    $('.catalog-results').slideUp(100);
    $('.sidebar_search input').val('');
    window.history.pushState(null, null, newUrl);
    $('main.catalog').addClass('loading');
    $.ajax({
        url: newUrl,
        method: 'get',
        contentType: 'application/json; charset=utf-8',
        success: function(response) {
            $('.products-group_wrapper').html(response);
            filterFormSubmit.text('Применить');
            $('main.catalog').removeClass('loading');
            if (smooth) {
                document.querySelector('main.catalog').scrollIntoView({
                    behavior: 'smooth'
                });
            }
            smooth = false;
            updateTitles();
        }
    });
});

function updateTitles(response) {
    const title = $(document).find('.hidden-titles .title').text();
    const mainTitle = $(document).find('.hidden-titles .main-title').text();
    $('head title').text(title);
    $('.section-header__title').text(mainTitle);
}

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
    return location.protocol + '//' + location.host + path + queryData + '/';
}

function getQueryData() {
    const filters = {};
    let strArr = [];
    if ($('.form-filters [name="price"]').length) {
        filters.price = [String($('.form-filters [name="price"]').val()).replace(';', '=')];
    }
    filters.page = [String($('.form-filters [name="page"]').val())];
    $('.form-filters input:checked').each(function() {
        const $this = $(this);
        const key = $this.attr('name');
        const value = $this.val();
        if (!filters[key]) {
            filters[key] = [];
        }
        filters[key].push(value);
    });
    filters.order = [$('#product-order').val()];
    for (const filter in filters) {
        const params = filters[filter].join('=');
        strArr.push(`${filter}:${params}`);
    }
    let result = strArr.join(';');
    return result;
}

function setPage(page=1) {
    filterForm.find('[name="page"]').val(page);
}

// pagination
$('main.catalog').on('click', '.page-links__item button:not(.manual)', function(e) {
    e.preventDefault();
    const page = $(this).attr('data-page');
    $(this).closest('.pagination').addClass('loading');
    setPage(page);
    filterForm.submit();
    smooth = true;
});

// ordering
$('#product-order').on('change', function() {
    setPage();
    filterForm.submit();
});