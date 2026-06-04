let android_app = new Vue(
    {
        el: "#android-app",
        data: {
            location: {
                latitude: '18',
                longitude: '9',
            },
        },
        mounted: function () {
            let location_s = Android.getLocation()
            this.location = JSON.parse(location_s)
            Android.showToast(location_s)
        },
        methods: {
            show_toast: function (message) {
                Android.showToast(message)

            },


            save_location: function () {
                let payload = {
                    profile_id: profile_id,
                    latitude: android_app.location.latitude,
                    longitude: android_app.location.longitude,
                    csrfmiddlewaretoken: csrfmiddlewaretoken
                }
                console.log(payload)
                var posting = $.post(url_save_location,payload);

                // Put the results in a div
                posting.done(function (data) {
                    console.log(data)
                    // word_app.word = (data.word);
                    // word_app.definitions = (data.definitions);
                    if (data.result === 'SUCCEED') {
                        Android.showToast("موقعیت شما با موفقیت ثبت شد.")

                    }
                })



            },
        },
    },
)