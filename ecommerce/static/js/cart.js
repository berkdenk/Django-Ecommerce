var updateBtns=document.getElementsByClassName('update-cart')

for (var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function () {
        var productId = this.dataset.product;
        var action = this.dataset.action;
        console.log('productId:', productId, 'Action:', action);

        console.log('USER:', user);
        if (user == 'AnonymousUser') {
            addCookieItem(productId, action); // Pass productId and action as arguments

        } else {
            updateUserOrder(productId, action);
        }
    });
}

function addCookieItem(productId, action) {
    console.log('Not logged in...');
    // Perform actions with productId and action as needed
    if (action === 'add') {
        if (cart[productId] === undefined) {
            cart[productId] = { 'quantity': 1 };
        } else {
            cart[productId]['quantity'] += 1;
        }
    }
    if (action === 'remove') {
        cart[productId]['quantity'] -= 1;
        if (cart[productId]['quantity'] <= 0) {
            console.log('Remove Item');
            delete cart[productId];
        }
    }
    console.log('Cart:', cart);

    // Manually set the SameSite attribute for the cookie
    const cookieString = 'cart=' + JSON.stringify(cart) + '; SameSite=None; Secure; domain=; path=/';
    
    // Set the cookie using JavaScript
    document.cookie = cookieString;
    location.reload()
}





function updateUserOrder(productId,action){
    console.log('User is authenticated,sending data....')

    var url='/update_item/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({'productId': productId, 'action': action}),
    })    
    .then((response)=>{
        return response.json();
    })
    .then((data)=>{
        console.log('data:',data)
        location.reload()
    })
    .catch((error) => {
        console.error('Error during fetch:', error);
    });
}