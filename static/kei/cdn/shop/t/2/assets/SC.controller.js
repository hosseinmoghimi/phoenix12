function SCController(params) {
    TiptoqueController.call(this, params);
    this.current_pickup_address = params.pickup_address;
}

SCController.prototype = _.assignIn(TiptoqueController.prototype, {

});