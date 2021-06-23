$(document).ready(function () {
    $('form#dep-form').on('submit', function (event){
       event.preventDefault();
       var title = document.getElementById('dep-form-title');
        var parent_id = document.getElementById('dep-form-par-id');
        $.ajax({
            url:"/get_departments",
            type: "POST",
            data: {title: title.value, parent_id: parent_id.value},
            dataType: 'json',
            success: function (resp){
             $('#departments').replaceWith(resp.data)
          }
        })
    });
});

