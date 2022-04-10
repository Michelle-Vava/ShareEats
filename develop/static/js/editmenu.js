var foodBtns = document.getElementsByClassName('get-food-item')
var user = '{{ request.user }}'
var availBtn = document.getElementsByClassName('item-availability')
//console.log(availBtn)
//console.log('{{request.session["product_item"]}}')

// product.value = 100;
for (var i = 0; i < availBtn.length; i++) {
  product_avl = availBtn[i].dataset.productavl
  console.log(product_avl)
  if (product_avl == "True") {
    //console.log("true")
    availBtn[i].innerHTML = "Active"
    availBtn[i].style.color = "green"
  } else {
    // console.log("False")
    availBtn[i].innerHTML = "Inactive"
    availBtn[i].style.color = "red"
  }



}

for (var i = 0; i < foodBtns.length; i++) {
  foodBtns[i].addEventListener('click', function () {
    var product = this.dataset.productname

    // console.log('product_name:', product)
    // console.log('USER', user)
    if (user == 'AnonymousUser') {
      //console.log("User is not authenticated")

    } else {
      //console.log("user is authenticated,sending data..")
      // var product = document.getElementById('id_product')
      // $("input[name=product]").val("hello")
      //product.setAttribute('value', 'defaultValue');
      console.log(product)
      product_name = product.split(",")
      console.log(product_name)
      $("input[name=product]").val(product_name[0])
      $("input[name=servings]").val(product_name[1])
      $("input[name=price]").val(product_name[2])
      $("input[name=category]").val(product_name[3])
      $("input[name=id]").val(product_name[5])
      $("#id_availability").val(product_name[6])
      // console.log($("input[name=id]").val)
      //   if(obj.options[i].value == "b"){
      //     obj.selectedIndex = i;
      // }

      //  .val()
      // $("input[name=image").val(product_name[4])
      // SelectItem(product)
    }

  })
}

