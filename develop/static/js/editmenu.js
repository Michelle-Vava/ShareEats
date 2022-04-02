var foodBtns = document.getElementsByClassName('get-food-item')
var user = '{{ request.user }}'

// product.value = 100;

for (var i = 0; i < foodBtns.length; i++) {
  foodBtns[i].addEventListener('click', function () {
    var product = this.dataset.productname   

    console.log('product_name:', product)
    console.log('USER', user)
    if (user === 'AnonymousUser') {
      console.log("User is not authenticated")

    } else {
      console.log("user is authenticated,sending data..")
     // var product = document.getElementById('id_product')
      // $("input[name=product]").val("hello")
      //product.setAttribute('value', 'defaultValue');
      //console.log(product)
      product_name = product.split(" ")
console.log(product_name)
      $("input[name=product]").val(product_name[0])
      $("input[name=servings").val(product_name[1])
      $("input[name=price").val(product_name[2])
      $("input[name=category").val(product_name[3])
      // $("input[name=image").val(product_name[4])
      // SelectItem(product)
    }

  })
}
function SelectItem(product_name) {
  

}

// function SelectItem(product_name) {
  
//   console.log(product)
//   // .innerHTML = 
//   //        "Value = " + "'" + inputF.value + "'el_down";
// }

// // function SelectItem(product_name) {

// //   newvalue = 100;



// // }

//   // fetch(url, {
//   //   method: "GET",

//   //   credentials: "same-origin",
//   //   body: JSON.stringify({ productname: product_name })
//   // })
//   //   .then(response => response.json())
//   //   .then(data => {
//   //     console.log(data)
//   //     //window.location.href = '/buyer/menu';
//   //     // location.reload()
//   //     //"/seller/item"
//   //     $('#edititem').modal('show')
//   //     // GET AJAX request
//   //     // $.ajax({
//   //     //     type: 'GET',
//   //     //     url: "{% url 'item editing' %}",
//   //     //     success: function (response) {
//   //     //          $('#edititem').modal('show')
//   //     //     },
//   //     //     error: function (response) {
//   //     //         console.log(response)
//   //     //     }
//   //     // })
//   //   })






// // $('#editMenu').on('show.bs.modal', function (event) {
// //   var button = $(event.relatedTarget) // Button that triggered the modal
// //   var recipient = button.data('productname') // Extract info from data-* attributes
// //   // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
// //   // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
// //   var modal = $(this)
// //   modal.find('.modal-title').text('New message to ' + recipient)
// //   modal.find('.modal-body input').val(recipient)
// // })