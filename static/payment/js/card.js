function card(stripe_published_key, customer_email) {
    document.addEventListener("DOMContentLoaded", function (event) {
        const stripe = Stripe(stripe_published_key);
        let elements = stripe.elements();

        let style = {
            base: {
                color: '#32325d',
                fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
                fontSmoothing: 'antialiased',
                fontSize: '16px',
                '::placeholder': {
                    color: '#aab7c4',
                }
            },
            invalid: {
                color: '#fa755a',
                iconColor: '#fa755a'
            }
        };

        let card = elements.create('card', { style: style, hidePostalCode: true });
        card.mount('#card-element');

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

            stripe.createToken(card).then(function (result) {
                if (result.error) {
                    let errorElement = document.getElementById('card-errors');
                    errorElement.textContent = result.error.message;
                } else {
                    stripe.createPaymentMethod({
                        type: 'card',
                        card: card,
                        billing_details: {
                            email: customer_email,
                        },
                    }).then(function (payment_method_result) {
                        if (payment_method_result.error) {
                            let errorElement = document.getElementById('card-errors');
                            errorElement.textContent = payment_method_result.error.message;
                        } else {
                            let form = document.getElementById('payment-form');
                            let hiddenInput = document.createElement('input');

                            hiddenInput.setAttribute('type', 'hidden');
                            hiddenInput.setAttribute('name', 'payment_method_id');
                            hiddenInput.setAttribute('value', payment_method_result.paymentMethod.id);

                            form.appendChild(hiddenInput);
                            form.submit();

                        }
                    })
                }
            })

        });

    })
}