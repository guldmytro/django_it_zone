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