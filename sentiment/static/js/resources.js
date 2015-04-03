$(function() {
  var navPosition = $('nav').offset().top;
  $(window).bind('scroll',function() {
    if($(window).scrollTop() > navPosition - $('#nav-phantom').height()) {
      $('nav').addClass('fixed');
      $('#nav-phantom').show();
    } else {
      $('nav').removeClass('fixed');
      $('#nav-phantom').hide();
    }
  });
});