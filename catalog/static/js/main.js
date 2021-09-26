$(document).ready(function() {

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

    // range slider
    $(".js-range-slider").ionRangeSlider({
        type: 'double',
        min: 10,
        max: 70000,
        postfix: ' ₽'
    });

    // filters
    $('.sidebar-filters__header').click(function() {
        const $this = $(this);
        $this.toggleClass('active').next('.sidebar-filters__items').slideToggle(200);
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
        $('.products-group').toggleClass('off');
    });

    // add to wishlist
    $('button.btn_add-to-wishlist').on('click', function(e) {
        e.preventDefault();
        $(this).toggleClass('active');
    });

    // controls btn
    $('.header-controls__btn').on('click', function(e) {
        e.preventDefault();
        const $this = $(this);

        if (!$this.hasClass('active')) {
            $('.header-controls__btn.active').removeClass('active');
            $('.products-group').removeClass('grid').removeClass('list').addClass($this.attr('data-class'));
            $this.addClass('active');
        }
    });

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

