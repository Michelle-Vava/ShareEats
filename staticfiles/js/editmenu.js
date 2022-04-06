 var foodBtns = document.getElementsByClassName('get-food-item')
   var user = '{{ request.user }}'

   for (var i=0; i< foodBtns.length;i++)
   {
       foodBtns[i].addEventListener('click',function(){
           var product = this.dataset.productname

           console.log('product_name:',product)
           console.log('USER', user)
           if (user === 'AnonymousUser') {
               console.log("User is not authenticated")

           } else{
               console.log("user is authenticated,sending data..")
               SelectItem(product)
           }

       })
   }
   function SelectItem(product_name){
        var url = '/seller/edititem'
      fetch(url, {
        method: "POST",

        credentials: "same-origin",
        body: JSON.stringify({productname: product_name})
      })
      .then(response => response.json())
      .then(data => {
        console.log(data)
          //window.location.href = '/buyer/menu';
           // location.reload()
           //"/seller/item"
       $('#edititem').modal('show')
        // GET AJAX request
        // $.ajax({
        //     type: 'GET',
        //     url: "{% url 'item editing' %}",
        //     success: function (response) {
        //          $('#edititem').modal('show')
        //     },
        //     error: function (response) {
        //         console.log(response)
        //     }
        // })
    })


   }