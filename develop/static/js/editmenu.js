//  var foodBtns = document.getElementsByClassName('get-food-item')
//    var user = '{{ request.user }}'

//    for (var i=0; i< foodBtns.length;i++)
//    {
//        foodBtns[i].addEventListener('click',function(){
//            var product = this.dataset.productname

//            console.log('product_name:',product)
//            console.log('USER', user)
//            if (user === 'AnonymousUser') {
//                console.log("User is not authenticated")

//            } else{
//                console.log("user is authenticated,sending data..")
//                SelectItem(product)
//            }

//        })
//    }
//    function SelectItem(product_name){
//         var url = '/seller/edititem'
//       fetch(url, {
//         method: "POST",

//         credentials: "same-origin",
//         body: JSON.stringify({productname: product_name})
//       })
//       .then(response => response.json())
//       .then(data => {
//         console.log(data)
//           //window.location.href = '/buyer/menu';
//            // location.reload()
//            //"/seller/item"
//        $('#edititem').modal('show')
//         // GET AJAX request
//         // $.ajax({
//         //     type: 'GET',
//         //     url: "{% url 'item editing' %}",
//         //     success: function (response) {
//         //          $('#edititem').modal('show')
//         //     },
//         //     error: function (response) {
//         //         console.log(response)
//         //     }
//         // })
//     })


//    }



$('#editMenu').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget) // Button that triggered the modal
  var recipient = button.data('productname') // Extract info from data-* attributes
  // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
  // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
  var modal = $(this)
  modal.find('.modal-title').text('New message to ' + recipient)
  modal.find('.modal-body input').val(recipient)
})