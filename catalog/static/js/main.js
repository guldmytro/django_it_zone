$(document).ready(function() {
    const csrftoken = $('[name="csrfmiddlewaretoken"]').val();
    function csrfSafeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
            }
        }
    });

    // banner
    $('.main-banner__brands').on('init', function() {
        $(this).addClass('inited');
    });
    $('.main-banner__brands').slick({
        infinite: true,
        slidesToShow: 4,
        slidesToScroll: 1,
        responsive: [
            {
                breakpoint: 992,
                settings: {
                    slidesToShow: 3,
                    slidesToScroll: 1,
                    infinite: true,
                }
            },
            {
                breakpoint: 768,
                settings: {
                    slidesToShow: 2,
                    slidesToScroll: 1,
                    infinite: true,
                }
            }
        ]
    });

    // product sliders
    $('.top-products__slider, .latest-products__slider').slick({
        infinite: true,
        slidesToShow: 4,
        slidesToScroll: 1,
        responsive: [
            {
                breakpoint: 1200,
                settings: {
                    slidesToShow: 3,
                    slidesToScroll: 1,
                    infinite: true,
                }
            },
            {
                breakpoint: 992,
                settings: {
                    slidesToShow: 2,
                    slidesToScroll: 1,
                    infinite: true,
                }
            },
            {
                breakpoint: 576,
                settings: {
                    slidesToShow: 1,
                    slidesToScroll: 1,
                    infinite: true,
                }
            }
        ]
    });

    // news slider
    $('.news-slider').slick({
        infinite: true,
        slidesToShow: 3,
        slidesToScroll: 1,
        responsive: [
            {
                breakpoint: 992,
                settings: {
                    slidesToShow: 2,
                    slidesToScroll: 1,
                    infinite: true,
                }
            },
            {
                breakpoint: 768,
                settings: {
                    slidesToShow: 1,
                    slidesToScroll: 1,
                    infinite: true,
                }
            }
        ]
    });

    // product slider
    $('.aside-gallery.gallery').slick({
        dots: false,
        infinite: true,
        speed: 600,
        slidesToShow: 3,
        slidesToScroll: 1,
        vertical: true,
        verticalSwiping: true,
        prevArrow: false,
        centerMode: true,
        centerPadding: '0px',
        cssEase: 'ease',
        asNavFor: '.main-product-gallery',
        responsive: [
            {
            breakpoint: 576,
            settings: {
                vertical: false,
                slidesToShow: 3,
                slidesToScroll: 1
            }
            }
        ]
    });
    const nav = $('.aside-gallery.gallery').length ? '.aside-gallery.gallery' : false;
    $('.main-product-gallery').on('beforeChange', function(event, slick, currentSlide, nextSlide) {
        if (!$('.aside-gallery.static').length) {
            return;
        }
        $('.aside-gallery.static .slick-current').removeClass('slick-current');
        $(`.aside-gallery.static [data-slick-index="${nextSlide}"]`).addClass('slick-current');

    });
    $('.main-product-gallery').slick({
        dots: false,
        infinite: true,
        speed: 600,
        slidesToShow: 1,
        slidesToScroll: 1,
        prevArrow: false,
        nextArrow: false,
        cssEase: 'ease',
        asNavFor: nav
    });

    $('.aside-gallery.gallery .aside-gallery__item').on('click', function() {
        const index = $(this).attr('data-slick-index');
        $('.aside-gallery').slick('slickGoTo', index);
    });

    $('.aside-gallery.static .aside-gallery__item').on('click', function() {
        const index = $(this).attr('data-slick-index');
        $('.main-product-gallery').slick('slickGoTo', index);
        $('.aside-gallery__item.slick-current').removeClass('slick-current');
        $(this).addClass('slick-current');
    });

    // header-menu
    $('.header-menu_btn').click(function() {
        $(this).toggleClass('active');
        $('.mobile-menu-wrapper').hide(150);
        $('.header-menu-wrapper').slideToggle(300);
        if (!$('.main-menu__item.active').length) {
            $('.main-menu__item:first-child').addClass('active');
        }
    });
    $('.main-menu__item').hover(function() {
        const $this = $(this);
        if (!$this.hasClass('active')) {
            $('.main-menu__item.active').removeClass('active');
            $this.addClass('active');
        }
    });

    $('.main-menu__item').click(function(e) {
        e.preventDefault();
        if (document.documentElement.clientWidth <= 991) {
            $(this).find('.main-menu__sub').slideToggle(300);
        }
    });

    $(window).resize(function() {
        if (document.documentElement.clientWidth > 991) {
            $('.main-menu__sub').css('display', 'block');
            $('.mobile-menu-wrapper').hide();
        } else {
            $('.main-menu__sub').css('display', 'none');
        }
    });

    $('.btn__mobile-menu').click(function(e) {
        e.preventDefault();
        $('.header-menu-wrapper').hide(150);
        $('.header-menu_btn.active').removeClass('active');
        $('.mobile-menu-wrapper').slideToggle(300);
    });

    $('.header-filters__btn').click(function(e) {
        e.preventDefault();
        $(this).toggleClass('active');
        $('.catalog__aside').toggleClass('active');
        $('.products-group_wrapper').toggleClass('off');
    });

    // controls btn
    $('.header-controls__btn').on('click', function(e) {
        e.preventDefault();
        const $this = $(this);

        if (!$this.hasClass('active')) {
            $('.header-controls__btn.active').removeClass('active');
            const currentClass = $this.attr('data-class');
            window.localStorage.setItem('catalog-layout', currentClass);
            $('.products-group_wrapper').removeClass('grid').removeClass('list').addClass(currentClass);
            $this.addClass('active');
        }
    });
    const catalogLayout = localStorage.getItem('catalog-layout');
    if (catalogLayout) {
        $(`.header-controls__btn[data-class="${catalogLayout}"`).click();
    }

    // product tabs
    $('.product-tabs__group button').on('click', function() {
        const $this = $(this);
        if ($this.hasClass('active')) {
            return false;
        }
        const id = $this.attr('data-id');
        const tabContent = $(`#${id}`);
        if (!tabContent.length) {
            return false;
        }
        $('.product-tabs__group button.active').removeClass('active');
        $('.tabs-content .tabs-content__item.active').removeClass('active');
        $this.addClass('active');
        tabContent.addClass('active');
    });
    $('.product-tabs__group button:first-child').click();

}); // end ready

// add to cart
// change quantity input
$('.quantity__group .inc').click(function() {
    const quantityInput = $(this).siblings('.quantity__input');
    quantityInput.val(Number(quantityInput.val()) + 1);
});

$('.quantity__group .decr').click(function() {
    const quantityInput = $(this).siblings('.quantity__input');
    let newValue = Number(quantityInput.val()) - 1;
    if (newValue < 1) {
        newValue = 1;
    }
    quantityInput.val(newValue);
});

$('body').on('submit', '.add-to-cart-form', function(e) {
    e.preventDefault();
    const $this = $(this);
    const action = $this.attr('action');
    const data = $this.serialize();
    const btn = $this.find('[type="submit"]');
    btn.prop('disabled', true).addClass('loading');
    $.ajax({
        url: action,
        method: 'post',
        data: data,
        success: function(response) {
            if (response.status === 'ok') {
                btn.prop('disabled', false).removeClass('loading').addClass('added');
                btn.text('Добавлено!');
                btn.siblings('.go-to-cart-link').addClass('active');
                updateCnt(response.cnt, $('.control-links__item.btn_cart-link .cnt'));
            }
        }
    });
});

function updateCnt(cnt, element) {
    let quantity = parseInt(cnt, 10);
    if (!isNaN(quantity)) {
        quantity = quantity > 9 ? '9+' : quantity;
        element.attr('data-cnt', quantity).text(quantity);
    }
}


$('body').on('submit', '.add-to-wishlist-form', function(e) {
    e.preventDefault();
    const $this = $(this);
    const action = $this.attr('action');
    const data = $this.serialize();
    const btn = $this.find('[type="submit"]');
    btn.prop('disabled', true).addClass('loading');
    $.ajax({
        url: action,
        method: 'post',
        data: data,
        success: function(response) {
            if (response.status === 'removed') {
                $this.find('[name="method"]').val('add');
                btn.removeClass('active');
            } else {
                $this.find('[name="method"]').val('remove');
                btn.addClass('active');
            }
            updateCnt(response.cnt, $('.header-controls__links .btn_add-to-wishlist .cnt'));
            btn.prop('disabled', false).removeClass('loading');
        }
    });
});
