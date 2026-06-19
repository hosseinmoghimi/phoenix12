function SCCartPanel(params) {
    PARTCartPanel.call(this, params);
    //$(this._.selectors.deliverySetup).addClass('hidden');
}
var _SCCartPanel = {
    emit: function (name) {
        console.log("%c→ EMIT SCCartPanel." + name,"background:#1e98ec;color:#FFF")
        console.log({arguments})
        $(document).trigger('SCCartPanel.' + name, arguments);
    }

}

SCCartPanel.prototype = _.merge(PARTCartPanel.prototype, _SCCartPanel);
console.log("%cRENDER SC.cart.js.liquid","background:yellow;color:#333")



