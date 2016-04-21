/* Javascript for OfficeVideoXBlock. */
function OfficeVideoXBlock(runtime, element) {

  var display_name = $(element).find('input[name=edit_display_name]');
  var video_url = $(element).find('input[name=edit_video_url]');
  var error_message = $(element).find('.officevideo-xblock .error-message');

  $(element).find('.save-button').bind('click', function() {
    var display_name_val = display_name.val().trim();
    var video_url_val = video_url.val().trim();

    clearErrors();

    if (!display_name_val) {
      display_name.addClass('error');
      error_message.addClass('visible');
      return;
    }

    if (!video_url_val || (!isValidUrl(video_url_val) && !isValidEmbedCode(video_url_val))) {
      video_url.addClass('error');
      error_message.addClass('visible');
      return;
    }

    var data = {
      display_name: display_name_val,
      video_url: video_url_val
    };

    var handlerUrl = runtime.handlerUrl(element, 'studio_submit');

    $.post(handlerUrl, JSON.stringify(data)).done(function(response) {
      window.location.reload(false);
    });
  });

  display_name.bind('keyup', function(){
    clearErrors();
  });

  video_url.bind('keyup', function(){
    clearErrors();
  });

  $('.cancel-button', element).bind('click', function() {
    runtime.notify('cancel', {});
  });

  function clearErrors() {
    display_name.removeClass('error');
    video_url.removeClass('error');
    error_message.removeClass('visible');
  }

  function isValidUrl(url) {
    return /^(https?):\/\/(((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:)*@)?(((\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5]))|((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.?)(:\d*)?)(\/((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)+(\/(([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)*)*)?)?(\?((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)|[\uE000-\uF8FF]|\/|\?)*)?(#((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)|\/|\?)*)?$/i.test(url);
  }

  function isValidEmbedCode(code) {
    return /<iframe /i.test(code);
  }


  $(function ($) {
    /* Here's where you'd do things on page load. */
  });
}
