if(typeof TASVIEH === "undefined"){

    let TASVIEH = 'تسویه'
}
let BEDEHKAR = 'بدهکار'
let BESTANKAR = 'بستانکار'
let TUMAN = 'تومان'
let RIAL = 'ریال'
let SUCCEED = "SUCCEED"
let FAILED = "FAILED"
var to_price = function (x, currency) {
    if (x == null)
        return ""
    if (typeof currency === 'undefined')
        currency = ''
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") + ' ' + currency
}

let copy_to_clipboard=function(vall,name){
    console.log(vall +' copied to clipboard')
    console.log('name='+name)
    console.log('vall='+vall)
    if(typeof name !='undefined'){
        let payload={
            csrfmiddlewaretoken:csrfmiddlewaretoken,
            text:vall,
            name:name,
        }
        let urll=url_add_clipboard_item
        $.post(urll,payload).done(data=>{
            console.log(data)
            if(data.result==='SUCCEED'){
                if(typeof clipboard_items_app !='undefined')
                    clipboard_items_app.clipboard_items.push({name:name,text:vall})
            }
        })
        clipboard.writeText(vall);

        console.log('saved')
    }
     
}
var to_price_colored = function (x, currency) {
    let color='muted'
    if (x == null)
        return ""
    if(x>0)color='success'
    if(x<0)color='danger'
    if (typeof currency === 'undefined')
        currency = ''
    let ssss= x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") + ' ' + currency
    return `<span class="text-${color}">${ssss}</span>`
}



var showNotification = function (from, align, icon, bgcolor, html, rtl = true,farsi=false) {
    
    if (rtl) html = `<div class="text-right`+(farsi?' farsi ':'')+`">` + html + `</div>`

    type = ['', 'info', 'danger', 'success', 'warning', 'rose', 'primary'];

    color = Math.floor((Math.random() * 6) + 1);
    color = 3;
    $.notify({
        icon: icon,
        message: html

    }, {
        type: bgcolor,
        timer: 20000,
        placement: {
            from: from,
            align: align
        }
    });
}