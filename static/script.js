var host_url = 'http://localhost:7778';
// var host_url = 'http://min.bz';


function populate_last3() {
    // alert("punim poslednja 3")
    // $("#xxx").append("<li>aaa</li>");
    //     $("#xxx").append("<li>aaa</li>");
    //
    //         $("#xxx").append("<li>aaa</li>");

    $.ajax({
               url: host_url+'/api/admin/last?limit=3',
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
    var shortenerInput  = $(".shorten-bg").val();

    populate_last3();

    $('#shorten').click(function () {

              $.ajax({
               url: host_url+'/api/short',
               type: 'PUT',
               data: { url: $('.shorten-bg').val()},
               success: function(response) {
                  var data = JSON.parse(response);
                  $('.copy-bg').val(host_url+'/r/' + data.id);

                  $("#last-three").append("<li>"+$('.shorten-bg').val()+"</li>");
               }
            });
    });

    $('#copy').click(function () {
      var copyText = document.getElementById("copybg");

      /* Select the text field */
      copyText.select();

      /* Copy the text inside the text field */
      document.execCommand("copy");
    });
});



