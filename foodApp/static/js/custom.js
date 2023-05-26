// let autocomplete;

// function initAutoComplete(){
// autocomplete = new google.maps.places.Autocomplete(
//     document.getElementById('id_address'),
//     {
//         types: ['geocode', 'establishment'],
//         //default in this app is "IN" - add your country code
//         componentRestrictions: {'country': ['in']},
//     })
// // function to specify what should happen when the prediction is clicked
// autocomplete.addListener('place_changed', onPlaceChanged);
// }

// function onPlaceChanged (){
//     var place = autocomplete.getPlace();

//     // User did not select the prediction. Reset the input field or alert()
//     if (!place.geometry){
//         document.getElementById('id_address').placeholder = "Start typing...";
//     }
//     else{
//         // console.log('place name=>', place.name)
//     }

//     // get the address components and assign them to the fields
//     // console.log(place);
//     var geocoder = new google.maps.Geocoder()
//     var address = document.getElementById('id_address').value

//     geocoder.geocode({'address': address}, function(results, status){
//         // console.log('results=>', results)
//         // console.log('status=>', status)
//         if(status == google.maps.GeocoderStatus.OK){
//             var latitude = results[0].geometry.location.lat();
//             var longitude = results[0].geometry.location.lng();

//             // console.log('lat=>', latitude);
//             // console.log('long=>', longitude);
//             $('#id_latitude').val(latitude);
//             $('#id_longitude').val(longitude);

//             $('#id_address').val(address);
//         }
//     });

//     // loop through the address components and assign other address data
//     console.log(place.address_components);
//     for(var i=0; i<place.address_components.length; i++){
//         for(var j=0; j<place.address_components[i].types.length; j++){
//             // get country
//             if(place.address_components[i].types[j] == 'country'){
//                 $('#id_country').val(place.address_components[i].long_name);
//             }
//             // get state
//             if(place.address_components[i].types[j] == 'administrative_area_level_1'){
//                 $('#id_state').val(place.address_components[i].long_name);
//             }
//             // get city
//             if(place.address_components[i].types[j] == 'locality'){
//                 $('#id_city').val(place.address_components[i].long_name);
//             }
//             // get pincode
//             if(place.address_components[i].types[j] == 'postal_code'){
//                 $('#id_pin_code').val(place.address_components[i].long_name);
//             }else{
//                 $('#id_pin_code').val("");
//             }
//         }
//     }

// }


$(document).ready(function(){
    $('.add_to_cart').on('click', function(e){
        e.preventDefault();
        food_id = $(this).attr('data-id');
        url = $(this).attr('data-url');


        $.ajax({
            type: 'GET',
            url: url,
            success: function(response){
                if(response.status == 'login_required') {
                    console.log(response)
                    Swal.fire({
                        title: response.message,
                        // text: 'Do you want to continue',
                        icon: 'info',
                        // confirmButtonText: 'Cool'
                      }).then(function(){
                        window.location = '/accounts/login';
                      })
                }
                else if(response.status == 'failed') {
                    Swal.fire({
                        title: response.message,
                        // text: 'Do you want to continue',
                        icon: 'error',
                        // confirmButtonText: 'Cool'
                      })
                }
                else{
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    $('#qty-'+food_id).html(response.qty);

                    // subtotal, tax, grand_total
                    applyCartAmounts(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax'],
                        response.cart_amount['grand_total']
                    );
                }

            }
        });
    })

    // decrease_cart
    $('.decrease_cart').on('click', function(e){
        e.preventDefault();
        food_id = $(this).attr('data-id');
        cart_id = $(this).attr('id');
        url = $(this).attr('data-url');
        $.ajax({
            type: 'GET',
            url: url,
            success: function(response){
                if(response.status == 'login_required') {
                    console.log(response)
                    Swal.fire({
                        title: response.message,
                        // text: 'Do you want to continue',
                        icon: 'info',
                        // confirmButtonText: 'Cool'
                      }).then(function(){
                        window.location = '/accounts/login';
                      })
                }
                else if(response.status == 'failed') {
                    Swal.fire({
                        title: response.message,
                        // text: 'Do you want to continue',
                        icon: 'error',
                        // confirmButtonText: 'Cool'
                      })
                }
                else{
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    $('#qty-'+food_id).html(response.qty);
                    if(window.location.pathname == '/marketplace/cart/') {
                        removeCartItem(response.qty, cart_id);
                        checkEmptyCart();
                    }
                    applyCartAmounts(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax'],
                        response.cart_amount['grand_total']
                    );
                }
            }
        });
    });

    // place the cart item quantity
    $('.item_qty').each(function(){
        var the_id = $(this).attr('id');
        var qty = $(this).attr('data-qty');
        $('#'+the_id).html(qty)

    });

    // delete_cart item
    $('.delete_cart').on('click', function(e){
        e.preventDefault();
        cart_id = $(this).attr('data-id');
        url = $(this).attr('data-url');
        $.ajax({
            type: 'GET',
            url: url,
            success: function(response){
                if(response.status == 'failed') {
                    Swal.fire({
                        title: response.message,
                        // text: 'Do you want to continue',
                        icon: 'error',
                        // confirmButtonText: 'Cool'
                      })
                }
                else {
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    Swal.fire({
                        title: response.message,
                        // text: 'Do you want to continue',
                        icon: 'error',
                        // confirmButtonText: 'Cool'
                      })
                    removeCartItem(0, cart_id);
                    checkEmptyCart();
                    applyCartAmounts(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax'],
                        response.cart_amount['grand_total']
                    );
                }
            }
        });
    })
    // delete the cart element if tthe qty is a
    function removeCartItem(cartItemQty, cart_id){
        if(cartItemQty <= 0) {

            //remove cart item
            document.getElementById("cart-item-"+cart_id).remove()
        }
    }
    function checkEmptyCart() {
        var cart_counter = document.getElementById("cart_counter").innerHTML
        if(cart_counter == 0) {
            document.getElementById("empty-cart").style.display = "block";
        }
    }

    // apply cart amounts

    function applyCartAmounts(subtotal, tax, grand_total) {
        if(window.location.pathname == '/marketplace/cart/') {
            $('#subtotal').html(subtotal);
            $('#tax').html(tax);
            $('#total').html(grand_total);
        }
    }

});