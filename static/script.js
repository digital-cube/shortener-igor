function populate_last3() {
    // alert("punim poslednja 3")
    // $("#xxx").append("<li>aaa</li>");
    //     $("#xxx").append("<li>aaa</li>");
    //
    //         $("#xxx").append("<li>aaa</li>");

    $.ajax({
               url: 'http://localhost:8802/api/admin/last?limit=3',
               type: 'GET',
                success: function(response) {
                    var data = JSON.parse(response);
                    console.log("data",data.list.length);

                    for (var i=0;i<data.list.length;i++) {
                        var adr = data.list[i][1];
                        console.log(i,adr);
                        $("#last-three").append("<li>"+adr+"</li>");
                    }

               }
            });

}

$(document).ready(function () {

    populate_last3();

    $('#create').click(function () {
              $.ajax({
               url: 'http://localhost:8802/api/short',
               type: 'PUT',
               data: { url: $('#url').val()},
               success: function(response) {
                  var data = JSON.parse(response);
                  $('#short-url').val('http://localhost:8802/r/' + data.id);

                  $("#last-three").append("<li>"+$('#url').val()+"</li>");
               }
            });
    });

    $('#copy').click(function () {
      var copyText = document.getElementById("short-url");

      /* Select the text field */
      copyText.select();

      /* Copy the text inside the text field */
      document.execCommand("copy");
    });
});
