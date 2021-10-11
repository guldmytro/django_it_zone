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
    const queryData = parseFilteredFields($this);
    const getParams = $this.serialize();
    const newUrl = getFilteredUrl($this);
    $('.catalog-results').slideUp(100);
    $('.sidebar_search input').val('');
    window.history.pushState(null, null, newUrl);
    $('main.catalog').addClass('loading');
    $.ajax({
        url: ".",
        method: 'post',
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify(queryData),
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
        }
    });
});

function getFilteredUrl(form) {
    const queryData = form.find('input:not([name="csrfmiddlewaretoken"])').serialize();
    return location.protocol + '//' + location.host + location.pathname + '?' + queryData;
}

function parseFilteredFields(form) {
    result = {}
    form.find('input').each(function() {
        const $this = $(this);
        if ($this.attr('name') === 'price') {
            result["price"] = {
                "key": "price",
                "values": [$this.val()]
            }
        }
        if (!$this.is(':checked') && $this.attr('name') != 'page') {
            return;
        }
        const key = $this.attr('name');
        const val = $this.val();
        if (!result[key]) {
            result[key] = {
                "key": key,
                "values": [val]
            }
        } else {
            result[key]['values'].push(val);
        }
    });
    const finalResult = [];
    for (let key in result) {
        finalResult.push(result[key]);
    }
    finalResult.push({
        "key": "full_path",
        "values": [form.serialize()]
    });
    return finalResult;
}

function setPage(page=1) {
    filterForm.find('[name="page"]').val(page);
}

// pagination
$('main.catalog').on('click', '.page-links__item a:not(.manual)', function(e) {
    e.preventDefault();
    const page = $(this).attr('data-page');
    $(this).closest('.pagination').addClass('loading');
    setPage(page);

    filterForm.submit();
    smooth = true;

});
