var updateBtns= document.getElementsByClassName('update-cart')

/* event listener */
for(var i=0;i<updateBtns.length;i++)
{
	updateBtns[i].addEventListener('click', function(){
		var productId= this.dataset.product /* data-"product" */
		var action= this.dataset.action
		console.log('productId:', productId, 'action:', action) /* check by adding to cart */

		//check if user is logged in or not
		console.log('USER:' , user)
		if(user === 'AnonymousUser'){
			console.log('not logged in')
		}else{
			updateUserOrder(productId, action)
		}
	})
}


function updateUserOrder(productId, action){
	console.log('User is logged in, sending data..')

	var url = '/update_item/'

	//post request
	fetch(url, {
		method : 'POST',
		headers:{
			'Content-Type':'application/json',
			'X-CSRFToken':csrftoken,
		},
		body:JSON.stringify({'productId': productId, 'action':action}) 
	})

	.then((response)=>{
		return response.json()
	})

	.then((data)=>{
		console.log('data:',data)
		location.reload()
	})
}
//log out fetch data, location.reload reloads the page