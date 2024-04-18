var hostname = window.location.host;
console.log(hostname)

function card(stripe_published_key, customer_email) {
    document.addEventListener("DOMContentLoaded", function (event) {
        // This is your test publishable API key.
        const stripe = Stripe(stripe_published_key);
        var elem = document.getElementById('submit');
        clientsecret = elem.getAttribute('data-secret');


        var elements = stripe.elements();
        var style = {
            base: {
                color: "#000",
                lineHeight: '2.4',
                fontSize: '16px'
            }
        };


        var card = elements.create("card", { style: style, hidePostalCode: true });
        card.mount("#card-element");

        card.on('change', function (event) {
            var displayError = document.getElementById('card-errors')
            if (event.error) {
                displayError.textContent = event.error.message;
                $('#card-errors').addClass('alert alert-info');
            } else {
                displayError.textContent = '';
                $('#card-errors').removeClass('alert alert-info');
            }
        });

        var form = document.getElementById('payment-form');

        form.addEventListener('submit', function (ev) {
            ev.preventDefault();

            let checkbox = document.getElementById("save-info");
            var custName = document.getElementById("fullName").value;
            var email = customer_email;
            var custAdd = document.getElementById("address1").value;
            var custAdd2 = document.getElementById("address2").value;
            var custAdd3 = document.getElementById("address3").value;
            var custAdd4 = document.getElementById("address4").value;
            var postCode = document.getElementById("zipcode").value;
            var payment_intent_id = document.getElementById("payment_intent_id").value;
            var payment_type = document.getElementById('payment_type').value;
            var amount = document.getElementById('amount').value;

            stripe.createToken(card).then(function (result) {
                if (result.error) {
                    let errorElement = document.getElementById('card-errors');
                    errorElement.textContent = result.error.message;
                } else {
                    stripe.createPaymentMethod({
                        type: 'card',
                        card: card,
                        billing_details: {
                            address: {
                                line1: custAdd,
                                line2: custAdd2 + custAdd3 + custAdd4,
                            },
                            name: custName,
                            email: email,
                        },

                    }).then(function (payment_method_result) {
                        if (payment_method_result.error) {
                            let errorElement = document.getElementById('card-errors');
                            errorElement.textContent = payment_method_result.error.message;
                        } else {
                            $.ajax({
                                type: "POST",
                                url: `/orders/add/`,
                                data: {
                                    order_key: clientsecret,
                                    csrfmiddlewaretoken: CSRF_TOKEN,
                                    fullname: custName,
                                    email: email,
                                    add1: custAdd,
                                    add2: custAdd2 + custAdd3 + " " + custAdd4,
                                    postcode: postCode,
                                    payment_method_id: payment_method_result.paymentMethod.id,
                                    payment_intent_id: payment_intent_id,
                                    payment_type: payment_type,
                                    amount: amount,
                                    action: "post",
                                },
                                success: function (json) {
                                    console.log(json.success)

                                    console.log('payment processed')
                                    // There's a risk of the customer closing the window before callback
                                    // execution. Set up a webhook or plugin to listen for the
                                    // payment_intent.succeeded event that handles any business critical
                                    // post-payment actions.
                                    window.location.href = '/payment/order_placed/'
                                },
                                error: function (xhr, errmsg, err) {
                                    console.log(errmsg)
                                }
                            })


                        }
                    })
                }
            })


            if (checkbox.checked) {
                $.ajax({
                    type: "POST",
                    url: `/account_update/`,
                    data: {
                        key: userid,
                        username: custName,

                        prefecture: custAdd,
                        city: custAdd2,
                        address1: custAdd3,
                        address2: custAdd4,
                        zipcode: postCode,
                        csrfmiddlewaretoken: CSRF_TOKEN,
                        action: "post",
                    },
                    success: function (json) {
                        console.log(json.success)

                    },

                    error: function (xhr, errmsg, err) {
                        console.log(errmsg)
                    }
                })
            }
        })

    })

}
