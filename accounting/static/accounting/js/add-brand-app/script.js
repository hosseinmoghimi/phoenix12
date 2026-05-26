 let add_brand_app = new Vue({
        el: "#add-brand-app",
        data: {
            name: "",
            show_form: false,
            message: { show: false },
        },
        methods: {
            add_brand: function () {
                let payload = {
                    csrfmiddlewaretoken: csrfmiddlewaretoken,
                    name: this.name,
                }
                console.log(payload)
                let posting = $.post(url_add_brand, payload)
                posting.done(data => {
                    
                    if (data.result === "SUCCEED") {
                        if (typeof brands_app != "undefined") {
                            brands_app.brands.push(data.brand)
                        }
                        show_message(add_brand_app, "موفقیت آمیز", data.message, "success", 5000)
                    }


                    if (data.result != "SUCCEED") {
                        show_message(add_brand_app, "خطا", data.message, "danger", 5000)
                    }

                })
            },
            to_price: function (vall) {
                return to_price(vall)
            }
        }
    })