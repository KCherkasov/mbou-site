$(document).on('click', '[data-spv-off]', function(){
  $.removeCookie('spv', { path: '/' });
  location.reload();
});

$(document).on('click', '[data-spv-on]', function(){
  $.cookie('spv', 1, {path:"/"});
  location.reload();
});

$(document).on('click', '[data-spv-setstyle]', function(){
  var $button = $(this);
  var style = $button.attr('data-spv-setstyle');
  $.cookie('colorstyle', style, {path: "/"});
  $('body').removeClass('wsite bsite csite').addClass(style);
  $('[data-spv-setstyle]').removeClass('active');
  $button.addClass('active');
  return false;
});

 $(document).on('click', '[data-spv-setfontsize]', function(){
  var $button = $(this);
  var style = $button.attr('data-spv-setfontsize');
  $.cookie('fontstyle', style, {path: "/"});
  $('body').removeClass('sfontsize mfontsize lfontsize').addClass(style);
  $('[data-spv-setfontsize]').removeClass('active');
  $button.addClass('active');
  return false;
});

$(document).on('change', '[data-spv-setimgstyle]', function(){
  var $button = $(this);
  var isSet = $button.is(':checked') ? 1 : 0;
  $.cookie('imgstyle', isSet, {path: "/"});
  if( isSet ){
    $('body').removeClass('imagesHidden');
  } else {
    $('body').addClass('imagesHidden');
  }
  return false;
});

$(document).on('change', '[data-spv-setbrail]', function(){
  var $button = $(this);
  var isSet = $button.is(':checked') ? 1 : 0;
  $.cookie('brailestyle', isSet, {path: "/"});
  if( isSet ){
    $('body').addClass('braileFont');
  } else {
    $('body').removeClass('braileFont');
  }
  return false;
});

$(document).ready(function () {
   if ($.cookie('spv')==="0") {
       $('body').removeClass('spv imagesHidden sfontsize mfontsize lfontsize wsite bsite csite');
       $('#spsettings').hide();
       $('#eyes').show();
   } else if ($.cookie('spv')==="1") {
        $('.prefoot.d-flex.align-items-center.flex-column').hide();
        $('#eyes').hide();
        if ($.cookie('fontstyle')==="sfontsize") {
            $('body').addClass('sfontsize');
        }
        if ($.cookie('fontstyle')==="mfontsize") {
            $('body').addClass('mfontsize');
        }
        if ($.cookie('fontstyle')==="lfontsize") {
            $('body').addClass('lfontsize');
        }
        if ($.cookie('colorstyle')==="wsite") {
            $('body').addClass('wsite');
        }
        if ($.cookie('colorstyle')==="bsite") {
            $('body').addClass('bsite');
        }
        if ($.cookie('colorstyle')==="csite") {
            $('body').addClass('csite');
        }
        if($.cookie('imgstyle')==="1") {
            $('body').addClass('imagesHidden');
        }
   }
});