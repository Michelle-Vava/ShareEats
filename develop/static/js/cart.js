var updateBtns = document.getElementsByClassName('update-cart')
var user = '{{ request.user }}'

for (var i = 0; i < updateBtns.length; i++) {
  updateBtns[i].addEventListener('click', function () {
    var productname = document.getElementById('output').innerHTML
    var quantity = 1

    console.log('product:', productname, 'quantity:', quantity)
    console.log('USER', user)
    if (user === 'AnonymousUser') {
      console.log("User is not authenticated")

    } else {
      console.log("user is authenticated,sending data..")
      updateUserOrder(productname, quantity)
    }

  })
}


var buyBtns = document.getElementsByClassName('update-modal')
for (var i = 0; i < buyBtns.length; i++) {
  buyBtns[i].addEventListener('click', function () {
    var productname = this.dataset.product
    var action = this.dataset.action
    var quantity = this.dataset.quantity
    var price = this.dataset.price
    var image = this.dataset.image
    console.log('product:', productname, 'Action', action, 'quantity:', quantity, 'image:', image)



    displaySelectedFood(productname, quantity, price, image)


  })
}
function updateUserOrder(productId, quantity) {
  var url = '/add-cart/'
  fetch(url, {
    method: "POST",

    credentials: "same-origin",
    body: JSON.stringify({ product: productId, quantity: quantity })
  })
    .then(response => response.json())
    .then(data => {
      console.log(data)
      location.reload()
      document.getElementById('response').innerHTML = "Item added to cart";
    })
}

function DecreaseQuantity() {
  var url = '/delete-cart/'
  fetch(url, {
    method: "POST",

    credentials: "same-origin",
    body: JSON.stringify({ product: productId, quantity: quantity })
  })
    .then(response => response.json())
    .then(data => {
      console.log(data)
      location.reload()
      document.getElementById('response').innerHTML = "Item added to cart";
    })
}
function RemoveItem() {
  var url = '/delete-cart/'
  fetch(url, {
    method: "POST",

    credentials: "same-origin",
    body: JSON.stringify({ product: productId })
  })
    .then(response => response.json())
    .then(data => {
      console.log(data)
      location.reload()
      document.getElementById('response').innerHTML = "Item added to cart";
    })
}
function IncreaseQuantity() {
  var url = '/delete-cart/'
  fetch(url, {
    method: "POST",

    credentials: "same-origin",
    body: JSON.stringify({ product: productId, quantity: quantity })
  })
    .then(response => response.json())
    .then(data => {
      console.log(data)
      location.reload()
      document.getElementById('response').innerHTML = "Item added to cart";
    })
}
function displaySelectedFood(productId, quantity, price, image) {
  var name = productId
  var quan = quantity
  var get_p = price
  var image_url = image


  document.getElementById('output').innerHTML = name;
  document.getElementById('quan').innerHTML = quan;
  document.getElementById('p').innerHTML = get_p;
  document.getElementsByName('product_image')[0].src = image_url;
}
$('#remove-item').on('click', function () {
  // $(this).parents("tr").remove();
  var input = $(this).parents("tr").find('input[type="text"]');
  console.log((input))
})
$(document).ready(function () {
  $('[data-toggle="tooltip"]').tooltip();
  var actions = $("table td:last-child").html();
  // Add row on add button click
  $(document).on("click", ".add", function () {
    IncreaseQuantity()
    /*
var empty = false;
var input = $(this).parents("tr").find('input[type="text"]');
    input.each(function(){
  if(!$(this).val()){
    $(this).addClass("error");
    empty = true;
  } else{
            $(this).removeClass("error");
        }
});
$(this).parents("tr").find(".error").first().focus();
if(!empty){
  input.each(function(){
    $(this).parent("td").html($(this).val());
  });
  $(this).parents("tr").find(".add, .edit").toggle();
}
     */
  });

  // Delete row on delete button click
  $(document).on("click", ".delete", function () {
    // $(this).parents("tr").remove();
    DecreaseQuantity()
  });
});