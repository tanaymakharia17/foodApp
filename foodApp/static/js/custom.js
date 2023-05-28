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
                        response.cart_amount['tax_dict'],
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
                        response.cart_amount['tax_dict'],
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
                        response.cart_amount['tax_dict'],
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

    function applyCartAmounts(subtotal, tax_dict, grand_total) {
        
        if(window.location.pathname == '/marketplace/cart/') {
            $('#subtotal').html(subtotal);
            $('#total').html(grand_total);
            for(key1 in tax_dict) {
                for(key2 in tax_dict[key1]) {
                    $('#tax-'+key1).html(tax_dict[key1][key2]+"("+key1+" %)");
                }
            }
        }
    }

    $('#add_hour').on('click', function(e){
        e.preventDefault();
        var day = document.getElementById('id_day').value;
        var from_hour = document.getElementById('id_from_hour').value;
        var to_hour = document.getElementById('id_to_hour').value;
        var is_closed = document.getElementById('id_is_closed').checked;
        var csrfmiddlewaretoken = document.getElementsByName('csrfmiddlewaretoken')[0].value;
        var url = document.getElementById('add_hour_url').value;
        console.log('is_closed=>', url);
        if(is_closed) {
            is_closed = 'True';
            condition = "day != ''";
        }
        else {
            is_closed = 'False';
            condition = "day != '' && from_hour != '' && to_hour != ''";
        }
        if (eval(condition)) {
            $.ajax({
                type: 'POST',
                url: url,
                data: {
                    'day': day,
                    'from_hour': from_hour,
                    'to_hour': to_hour,
                    'is_closed': is_closed,
                    'csrfmiddlewaretoken': csrfmiddlewaretoken
                },
                success: function(response){
                    console.log(response);
                    if(response.status == 'success') {
                        if(response.is_closed == 'Closed'){
                        html = '<tr id="hour-'+response.id+'"><td><b>'+response.day+'</b></td><td>Closed</td><td><a href="#" class="remove_hour btn btn-sm btn-danger" data-url="/vendor/opening-hours/remove/'+response.id+'/">Remove</a></td></tr>';
                        }
                        else{
                            html = '<tr id="hour-'+response.id+'"><td><b>'+response.day+'</b></td><td>'+response.from_hour+' - '+response.to_hour+'</td><td><a href="#" class="remove_hour btn-sm btn btn-danger" data-url="/vendor/opening-hours/remove/'+response.id+'/">Remove</a></td></tr>';
                        }
                        
                        $(".opening_hours").append(html)
                        document.getElementById("opening_hours").reset();
                    }
                    else {
                        Swal.fire({
                            title: response.message,
                            // text: 'Do you want to continue',
                            icon: 'error',
                            // confirmButtonText: 'Cool'
                        })
                    }
                }
            });
        }
        else {
            Swal.fire({
                title: "Please fill all the fields",
                icon: "info"
            });
        }
        // $.ajax({
        //     type: 'POST',
        //     url: 'opening-hours/add/'
        // });
    });

    // REMOVE OPENING HOUR
    $(document).on('click', '.remove_hour', function(e){
        e.preventDefault();
        url = $(this).attr('data-url');
        
        $.ajax({
            type: 'GET',
            url: url,
            success: function(response){
                if(response.status == 'success'){
                    document.getElementById('hour-'+response.id).remove()
                }
            }
        })
    })


});