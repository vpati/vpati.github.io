/* iseclab.js */

$(document).ready(function () {
    var homeSwiper = new Swiper('#home-slider', {
        slidesPerView: 'auto',
        spaceBetween: 1,
        autoplay: 2500
    });

    $('.publication-toggler').on('click', function(event){
        event.stopPropagation();
        var klass = '.' + $(this).attr('href').substring(1);
        $('.publication-inline').hide();
        $(klass).show();
    });
});
