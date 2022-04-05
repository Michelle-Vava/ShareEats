 var menuBtns = document.getElementsByClassName('get-menu')
   var user = '{{ request.user }}'

   for (var i=0; i< menuBtns.length;i++)
   {
       menuBtns[i].addEventListener('click',function(){
           var business = this.dataset.business

           console.log('businessname:',business)
           console.log('USER', user)
           if (user === 'AnonymousUser') {
               console.log("User is not authenticated")

           } else{
               console.log("user is authenticated,sending data..")
               ViewMenu(business)
           }

       })
   }


   function ViewMenu(business_name){
        var url = '/menu/'
      fetch(url, {
        method: "POST",

        credentials: "same-origin",
        body: JSON.stringify({businessname: business_name})
      })
      .then(response => response.json())
      .then(data => {
        console.log(data)
          window.location.href = '/buyer/menu';

      })
   }


