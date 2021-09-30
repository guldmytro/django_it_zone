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
const filterForm = $('.form-filters');
const filterFormSubmit = filterForm.find('[type="submit"]');
filterForm.find('input').on('change', function() {
    if (filterFormSubmit.is(':disabled')) {
        filterFormSubmit.prop('disabled', false);
    }
});

filterForm.submit(function(e) {
    e.preventDefault();
    const $this = $(this);
    filterFormSubmit.prop('disabled', true).text('Загрузка...');
    const queryData = parseFilteredFields($this);
//    window.location.href = getFilteredUrl(queryData);
    $.ajax({
        url: ".",
        method: 'post',
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify(queryData),
        success: function (response) {
            $('.products-group_wrapper').html(response);
            filterFormSubmit.text('Применить');
        }
    });
});

function getFilteredUrl(queryData) {
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
        if (!$this.is(':checked')) {
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
    return finalResult;
}

