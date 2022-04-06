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
      $('#DishModal').modal('show')
      // location.reload()
      document.getElementById('response').innerHTML = "Item added";
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

function updateQuantity(productId, quantity) {

  var url = '/modify-item/'
  fetch(url, {
    method: "POST",

    credentials: "same-origin",
    body: JSON.stringify({ product: productId, quantity: quantity })
  })
    .then(response => response.json())
    .then(data => {
      //console.log(data)
      //console.log(data["cartItems"])
      //console.log(data.cartItems)

      //var obj = JSON.parse(data);
      document.getElementById('cart-items').innerHTML = data.cartItems
      document.getElementById('cart-total').innerHTML = "$" + data.cartTotal
      document.getElementById(productId).innerHTML = quantity

    })
}


function increaseValue(productId) {

  var quantity = document.getElementById(productId).innerHTML
  //console.log(productId, quantity)
  //var value = parseInt(document.getElementById('number').value, 10);
  quantity = isNaN(quantity) ? 0 : quantity;
  quantity++;
  updateQuantity(productId, quantity)
  //console.log(d)
  //var id = 'decrease'

  // var value = parseInt(document.getElementById('number').value, 10);
  // value = isNaN(value) ? 0 : value;
  // value++;
  // document.getElementById('number').value = value;
  //document.location.reload()
}

function decreaseValue(productId) {
  var quantity = document.getElementById(productId).innerHTML
  console.log(productId, quantity)
  console.log(document.getElementById('cart-items'))
  console.log(document.getElementById('cart-items').value)

  // var value = parseInt(document.getElementById('number').value, 10);
  quantity = isNaN(quantity) ? 0 : quantity;
  quantity--;
  quantity < 1 ? quantity = 1 : '';

  updateQuantity(productId, quantity)
  //document.location.reload()

}