// Generated by CoffeeScript 1.3.3
(function() {

  $(document).ready(function() {
    var add_remove, inventory_number, label, tag_add_remove, _i, _len;
    tag_add_remove = function(tag_select, tag_wrapper, target_form) {
      $(tag_select).change(function(e) {
        add_remove($(e.target).val(), tag_wrapper, target_form);
      });
    };
    tag_add_remove('.tags', '#tag_wrapper', '#hardware_form');
    add_remove = function(tag, tag_wrapper, target_form) {
      $(tag_wrapper).append('<a href="' + tag + '" class="remove_tag btn btn-mini btn-info" style="margin-bottom: 5px;">' + tag + ' <i class="icon-remove-sign icon-white"></i></a> ');
      $(target_form).append('<input type="hidden" name="tag" value="' + tag + '"/>');
      $('.remove_tag').click(function(e) {
        e.preventDefault();
        if ($(e.target).hasClass('remove_tag')) {
          $(e.target).remove();
          $('input[value="' + $(e.target).attr('href') + '"]').remove();
        } else {
          $(e.target).parent().remove();
          $('input[value="' + $(e.target).parent().attr('href') + '"]').remove();
        }
      });
    };
    if (edit || copy) {
      for (_i = 0, _len = labels.length; _i < _len; _i++) {
        label = labels[_i];
        add_remove(label, '#tag_wrapper', '#hardware_form');
      }
    }
    inventory_number = $('.inventory_number').val();
    $('.submit').click(function(e) {
      var not_fullfilled_yet;
      e.preventDefault();
      not_fullfilled_yet = [];
      $('.check').each(function(index, value) {
        if (!$(value).val()) {
          not_fullfilled_yet.push($(value).parent().children('label').text());
        }
      });
      if (not_fullfilled_yet.length > 0) {
        alert('Bitte noch ' + not_fullfilled_yet.join(', ') + ' ausfüllen.');
        return;
      }
      if (edit && $('.inventory_number').val() === inventory_number) {
        $('#hardware_form').submit();
        return;
      }
      $.post('/hardware/invn/', {
        number: $('.inventory_number').val()
      }, function(data) {
        if (data === 'true') {
          alert('Inventarnummer schon vorhanden.');
          return;
        }
        $('#hardware_form').submit();
      });
    });
  });

}).call(this);
