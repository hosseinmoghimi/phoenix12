function TiptoqueController(params) {
    $.extend(this, params);
    this.init();
}

TiptoqueController.prototype = {
    _: {
        debounceTimeValue: 300,
        vendorBonCadeau:"Chef Bon Cadeau",
        deliveryProductType:"Livraison"
    },

    get DateValidCart() {
        if(!this.cart.attributes._createAt){
            return false
        }else{
            dateCreateAt = new Date(this.cart.attributes._createAt)
            dateCreateAt = new Date(dateCreateAt)
            timeCreateAt =  window._TOOLS.dateDiff(dateCreateAt,window._TOOLS.DATE_NOW)
            console.log({dateCreateAt,timeCreateAt: timeCreateAt.day,now:window._TOOLS.DATE_NOW,delCart:limit_count_date})

            if(timeCreateAt.day > limit_count_date){
                return false
            }
        }

        //verifier si la date du panier si elle est correcte par rapport a la date aujourd
        diffDates= this.DateDiffCart
        if(diffDates==undefined){
            return false
        }
        // limit_count_date   variable dans settings vendor du customize
        return diffDates.day >= 1
    },
    get DateDiffCart() {
        //verifier si la date du panier si elle est correcte par rapport a la date aujourd
        if(!!this.cart && !!this.cart.attributes && !!this.cart.attributes.Date){
            dateOrder = window._TOOLS.strToDate(this.cart.attributes.Date,'00')
            return window._TOOLS.dateDiff(window._TOOLS.DATE_NOW,dateOrder)
        }
        return undefined
    },

    get deliveryType() {
        return this.cart.attributes._deliveryType;
    },
    get deliveryProducts() {
        return _.filter(this.cart.items, {product_type: 'Livraison'})
    },
    get feesProducts() {
        return _.filter(this.cart.items, {product_type: 'frais_de_gestion'})
    },
    get deliveryProduct() {
        return this.deliveryProducts[0];
    },

    get countProducts(){
        return _.filter(this.cart.items, (o)=>!['Livraison','frais_de_gestion' ].includes(o.product_type)).length
    },
    get countProductTT(){
        return this.ProductisTT.length
    },
    get countProductNotTT(){
        return this.ProductisNotTT.length
    },
    get countProductMagic(){
        return this.ProductMagic.length
    },
    get countProductGiftCard(){
        return this.ProductGiftCard.length
    },

    get countDelivery(){
        return _.filter(this.cart.items, (o)=>o.product_type==='Livraison').length
    },
    get priceDelivery(){
        if(!!this.deliveryProduct){
            return parseInt(this.deliveryProduct.price/100)
        }
        return 0
    },

    get countFees(){
        return _.filter(this.cart.items, (o)=>o.product_type==='frais_de_gestion').length
    },
    get priceFees(){
        if(!!this.feesProducts){
            return parseFloat(this.feesProducts[0].price/100)
        }
        return 0
    },

    get ProductsAll(){
        return _.filter(this.cart.items, (o)=>!['Livraison','frais_de_gestion' ].includes(o.product_type))
    },

    get ProductisTT(){
        return _.filter(this.cart.items, (o)=>!!o.properties && !!o.properties._is_tt && o.properties._is_tt==="true")
    },
    get ProductisNotTT(){
        return _.filter(this.cart.items, (o)=> !["Carte Cadeau","Carte cadeau","carte cadeau","Gift Cards","gift cards","Livraison","frais_de_gestion"].includes(o.product_type) && (!o.properties || !o.properties._is_tt || o.properties._is_tt==="false") )
    },
    get ProductGiftCard(){
        return _.filter(this.cart.items, (o)=>!["Livraison" ,"frais_de_gestion"].includes(o.product_type) && ["Carte Cadeau","Carte cadeau","carte cadeau","Gift Cards","gift cards"].includes(o.product_type) && (!o.properties || !o.properties._is_tt || o.properties._is_tt==="false") )
    },
    get ProductMagic(){
        return _.filter(this.cart.items, (o)=>!!o.properties && !!o.properties._is_magic && o.properties._is_magic==="true")
    },

    get priceGiftCard(){
        return this.ProductGiftCard
            .map((el)=>(el.price * el.quantity)/100)
            .reduce(function(a, b){
                return a+b;
            }, 0);
    },
    get priceTTProduct(){
        return this.ProductisTT
            .map((el)=>(el.price * el.quantity)/100)
            .reduce(function(a, b){
                return a+b;
            }, 0);
    },
    get priceNotTTProduct(){
        return this.ProductisNotTT
            .map((el)=>(el.price * el.quantity)/100)
            .reduce(function(a, b){
                return a+b;
            }, 0);

    },
    get priceMagicProduct(){
        return this.ProductMagic
            .map((el)=>(el.price * el.quantity)/100)
            .reduce(function(a, b){
                return a+b;
            }, 0);
    },
    get countQty(){
        return this.ProductsAll
            .map((el)=>el.quantity)
            .reduce(function(a, b){
                return a+b;
            }, 0);
    },
    get vendor() {
        var vendors = this.getVendor(TT.cart);
        return _.first(vendors);

        //     var item = _.find(TT.cart.items, function (item) { return item.vendor !== this._.vendorBonCadeau && item.product_type !== this._.deliveryProductType; })
        //     return item && item.vendor
    },

    get strDateDelivery(){
        if(!!this.cart.attributes.Heure && this.cart.attributes.Date){
            var filterHour = _TOOLS.replaceAll(this.cart.attributes.Heure,":00","h");
            var heure =  filterHour.replace("-","/");

            if(this.cart.attributes._deliveryType === "delivery"){
                return "Pour le "+this.cart.attributes.Date+" entre "+heure;
            }
            return "Rendez-vous le "+this.cart.attributes.Date+" à "+ heure;
        }
        return "...";
    },
    debug:function(){
        console.table({
            deliveryType:this.deliveryType,
            countProducts:this.countProducts,
            countProductTT:this.countProductTT,
            countProductNotTT:this.countProductNotTT,
            countDelivery:this.countDelivery,
            priceDelivery:this.priceDelivery,
            countFees:this.countFees,
            priceFees:this.priceFees,
            priceTTProduct:this.priceTTProduct,
            priceNotTTProduct:this.priceNotTTProduct,
            vendor:this.vendor,
            strDateDelivery:this.strDateDelivery
        })
    },
    emit: function (name) {
        console.log("%c→ EMIT TT." + name,"background:#1e98ec;color:#FFF")
        console.log({method:"EMIT TT." + name,arguments})
        $(document).trigger('TT.' + name, arguments);
    },
    isZipValid: function (zip) {
        return !!zip && zip.length === 5;
    },
    clearCart: function () {
        var $d = $.Deferred();
        CartJS.clear({
            success: _.bind(function () {
                this.emit('clearItems');
                CartJS.clearAttributes({
                    success: _.bind(function () {
                        this.cart=CartJS.cart
                        this.emit('clearAttributes');
                        this.emit('clearCart');
                        $d.resolve();
                    }, this)
                })
            }, this)
        });
        return $d;
    },
    clearTTCart: function () {

        console.log("%c→ RUN TT.clearTTCart" ,"background:#1e98ec;color:#FFF")
        var $d = $.Deferred();
        var removeProduct ={};

        if(!!this.ProductisTT){
            _.each(Object.values(this.cart.items),_.bind(function(item,idx){
                if((item.product_type !== "Livraison" && !!item.properties._is_tt && item.properties._is_tt === "true" )|| item.product_type === "Livraison"){
                    removeProduct[item.variant_id] = 0;
                    if(!!this.bufferCart && !!this.bufferCart[item.variant_id]){
                        delete this.bufferCart[item.variant_id]
                    }
                    // delete this.cart.items[idx];
                    this.cart.items[idx].quantity = 0
                }
            },this))
        }

        if(!!removeProduct){
            CartJS.updateItemQuantitiesById(removeProduct, { success: _.bind(function() {
                    CartJS.clearAttributes({
                        success: _.bind(function (cart) {
                            console.log({cart})
                            this.cart = this.processCart(cart);
                            this.renderBubbleQty()
                            this.emit('clearAttributes');
                            this.emit('removeTTProducts',removeProduct);
                            $d.resolve();
                        }, this)
                    })
                }, this)
            });
        }else{
            CartJS.clearAttributes({
                success: _.bind(function (cart) {
                    console.log({cart})
                    this.cart = this.processCart(cart);
                    this.emit('clearAttributes');
                    $d.resolve();
                }, this)
            })
        }
        return $d;
    },
    clearItems:function(){
        var $d = $.Deferred();
        CartJS.clear({
            success: _.bind(function () {
                this.emit('clearItems');
                this.emit("itemUpdated.cartPanel");
                this.cart = this.processCart(CartJS.cart);
            }, this)
        });
        return $d;
    },
    validateCheckoutCartAttributes: function () {
        var attr = this.cart.attributes || {};
        if(!attr._deliveryType){
            return false;
        }
        //  return !!attr.Adresse && !!attr.Date && !!attr.Heure && !!attr.origin && !!attr.zip;
        if(attr._deliveryType ==="delivery"){
            return !!attr.Date && !!attr.Heure && !!attr.zip && !!attr._zone &&  attr._zone!=="false" ;
        }else{
            return !!attr.Date && !!attr.Heure ;
        }
    },
    validateFilterCartAttributes: function () {
        var attr = this.cart.attributes || {};
        return !!attr.Date && !!attr.Heure && !!attr._deliveryType ;

    },
    checkFiltersValidation: function () {
        if(!this.validateFilterCartAttributes()) {
            this.emit('filtersShowError');
        }
    },
    validateFilters: function (filters) {
        return !!filters.deliveryType && !!filters.date && !!filters.hour
        // return !!filters.zip && !!filters.city && !!filters.date && !!filters.deliveryType && !!filters.hour && !!filters.place
    },
    publicFilters: {zip: 'zip', place: 'Adresse', date: 'Date', hour: 'Heure', additional_info: 'Mes informations complémentaires'},
    removeDeliveryProducts: function () {
        var $d = $.Deferred()
        var toDelete = {}
        _.each(this.deliveryProducts, function (item) { toDelete[item.id] = 0; });
        CartJS.updateItemQuantitiesById(toDelete, { success: _.bind(function(cart) {
                this.cart = this.processCart(cart);
                this.emit('update.removeDeliveryProducts');
                $d.resolve();
            }, this)
        });
        return $d;
    },
    removeFeesProducts: function () {
        var $d = $.Deferred()
        var toDelete = {}
        _.each(this.feesProducts, function (item) { toDelete[item.id] = 0; });
        CartJS.updateItemQuantitiesById(toDelete, { success: _.bind(function(cart) {
                this.cart = this.processCart(cart);
                this.emit('update.removeFeesProducts');
                $d.resolve();
            }, this)
        });
        return $d;
    },
    getDeliveryProductZone: function (product, zip) {
        //verifier si le vendor correspond au produit dans le panier
        if(!zip || !product || zip.length !== 5) { return false; }
        var zipGroups = (product.content || product.product_description).split('|');
        var longZip = ',' + zip + ',';
        var shortZip = ',' + zip.slice(0, 2) + ',';
        var index = _.findIndex(zipGroups, function (group) { group = ',' + group + ','; return group.indexOf(longZip) !== -1 || group.indexOf(shortZip) !== -1 }) + 1;
        return !!index ? 'Z' + index : false;
    },
    getZipAppropriateDeliveryVariant: function (zip) {
        var zone = this.getDeliveryProductZone(deliveryProduct, zip);

        this.setAttributes({_zone:zone})
        return _.find(deliveryProduct.variants, {title: zone});
    },
    addDeliveryProduct: function (deliveryVariant) {
        var $d = $.Deferred();
        if(!deliveryVariant){
            deliveryVariant = this.getZipAppropriateDeliveryVariant(this.cart.attributes.zip);
        }
        if(!deliveryVariant) {
            $d.resolve();
        } else {
            var toUpdate = {};
            toUpdate[deliveryVariant.id] = 1;
            CartJS.updateItemQuantitiesById(toUpdate, {success: _.bind(function(cart) {
                    this.cart = this.processCart(cart);
                    this.emit('update.addDeliveryProduct');
                    $d.resolve();
                }, this)});
        }
        return $d;
    },

    addFeesProduct: function () {
        var $d = $.Deferred();
        console.log({prodFees})
        var feesVariant = prodFees?.variants[0] || null
        if(!feesVariant) {
            $d.resolve();
        } else {
            var toUpdate = {};
            toUpdate[feesVariant.id] = 1;
            CartJS.updateItemQuantitiesById(toUpdate, {success: _.bind(function(cart) {
                    this.cart = this.processCart(cart);
                    this.emit('update.addFeesProduct');
                    $d.resolve();
                }, this)});
        }
        return $d;
    },


    isZipDelivered: function (zip) {
        return !!this.getDeliveryProductZone(deliveryProduct, zip)
    },
    adaptFees:function(){
        console.log('Test sur le fees')
        if(this.countFees === 0 && this.countProducts > 0  ){
            this.addFeesProduct()
        }else if(this.countFees > 0 && this.countProducts === 0  ){
            //si existe un produit de frais de gestion pas de produit
            // je supprime tous et je remplace avec le nouveau produit fees si existant (car c un produit obligatoir)
            this.removeFeesProducts()
        }else if(prodFees == null){
            //si plus de produit fees au court du temp je le supprime ou je la joute si pas de produit dans le panier
            this.removeFeesProducts()
        }
    },
    adaptDelivery: function () {
        var $d = $.Deferred();
        if(this.deliveryType === 'delivery' && !!this.cart.attributes.zip && this.countProductTT>0) {
            //si le filtre et en mode delivery et qu il existe des produits dans le panier
            if(this.countProducts === 0 ){
                if(!this.getDeliveryProductZone(deliveryProduct, this.cart.attributes.zip)) {
                    this.emit('unhandledZip');
                    $d.resolve();
                    return $d;
                }
                $d.then(_.bind(function(){
                    this.emit('handledZip');
                }, this))
                if(this.countDelivery === 0 ) {
                    // Pas de livraison, on ajoute
                    this.addDeliveryProduct().then(_.bind($d.resolve), this);
                }
                else if(this.countDelivery > 1 ) {
                    // Plus de une livraison, on supprime tout et on ajoute
                    this.removeDeliveryProducts().then(_.bind(function () {
                        this.addDeliveryProduct().then(_.bind($d.resolve, this));
                    }, this))
                }
                else {
                    // Ici on a bien 1 livraison, on check si elle est bonne
                    var currentZone = this.getDeliveryProductZone(this.deliveryProduct, this.cart.attributes.zip);
                    if(!!this.deliveryProduct &&
                        !!deliveryProduct &&
                        deliveryProduct.id === this.deliveryProduct.id &&
                        currentZone === this.deliveryProduct.variant_title) {
                        $d.resolve();
                    } else {
                        this.removeDeliveryProducts().then(_.bind(function () {
                            this.addDeliveryProduct().then(_.bind($d.resolve, this));
                        }, this))
                    }
                }



            }
            else {
                // si les produits ne correspond pas au bon vendor
                if(!!deliveryProduct  && !_.includes(this.getVendor(), deliveryProduct.vendor)) {
                    //   console.trace({msg:"ERREUR changePageVendorWithOtherProductsIntoCart" , deliveryProduct})
                    this.emit("changePageVendorWithOtherProductsIntoCart");
                    $d.resolve();
                    return $d;
                }
                else if(!!deliveryProduct && this.countDelivery === 0) {
                    //ajouter le produit delivery
                    this.addDeliveryProduct().then(_.bind($d.resolve, this));
                }
                else {
                    // Ici on a bien 1 livraison, on check si elle est bonne
                    var currentZone = this.getDeliveryProductZone(this.deliveryProduct, this.cart.attributes.zip);

                    // console.log({msg:"adaptDelivery", currentZone, deliveryProduct, tt_deliveryProduct:this.deliveryProduct})
                    if(!!this.deliveryProduct && !!deliveryProduct &&
                        (deliveryProduct.id === this.deliveryProduct.id) &&
                        currentZone === this.deliveryProduct.variant_title) {
                        $d.resolve();
                    } else {
                        /*
                        this.removeDeliveryProducts().then(_.bind(function () {
                            this.addDeliveryProduct().then(_.bind($d.resolve, this));
                        }, this))
                        */
                    }
                }


            }
            // 3. suppression / modifications necessaires

        }
        else if (this.deliveryProduct) {
            //  this.removeDeliveryProducts();
            this.removeDeliveryProducts().then(_.bind(function () {
                //supprimer les informations de la zone de livraison pour TT
                delete this.cart.attributes.zip
                delete this.cart.attributes._zone
                delete CartJS.cart.attributes.zip
                delete CartJS.cart.attributes._zone
                this.emit('itemCartUpdated')
            }, this))
        }


        $d.resolve();

        return $d;
    },

    prepareAttributes: function (attributes) {
        _.each(attributes, function (val, k) {
            attributes[k] = val && val.split && val.split(',').join('__') || val;
            if(k === 'Date' && val.indexOf('-') !== -1) {
                var date = val.split('-');
                attributes[k] = [date[2], date[1], date[0]].join('/');
            }
        });
        return attributes;
    },
    setAttributes: function (attr) {
        var $d = $.Deferred();

        attr = this.prepareAttributes(attr)
        CartJS.setAttributes(_.assignIn(this.cart.attributes, attr), {
            success: _.bind(function () {
                this.cart = this.processCart(CartJS.cart);
                _.each(this.cart.attributes, _.bind(function (val, k) { this.cart.attributes[k] = val && val.split ? val.split('__').join(',') : val}, this));
                $d.resolve();
            }, this)
        });
        return $d;
    },

    processCart: function (cart) {
        for(var k in cart.attributes) {
            if(cart.attributes[k].split) {
                cart.attributes[k] = cart.attributes[k].split('__').join(',')
            }
        }
        return cart;
    },
    setFiltersAttributes: function (filters) {
        var $d = $.Deferred();
        if(filters.submit) {
            var attributes = {};
            for(var f in filters) {
                var k = this.publicFilters[f] || '_' + f;
                attributes[k] = filters[f];
            }
            //  if(attributes.Date && attributes.Date !== this.cart.attributes.Date) { CartJS.clear(); }
            attributes = this.prepareAttributes(attributes)
            CartJS.setAttributes(_.assignIn(this.cart.attributes, attributes), {
                success: _.bind(function (cart) {
                    this.cart = this.processCart(cart);
                    this.adaptFees();
                    this.adaptDelivery().then(_.bind(function () {
                        this.cart = this.processCart(this.cart);
                        this.emit('filtersValidated', filters);
                        $d.resolve();
                    }, this));
                    console.log('Test sur le fees')
                    if(this.countFees > 0 && this.countProducts === 0  ){
                        //si existe un produit de frais de gestion pas de produit
                        // je supprime tous et je remplace avec le nouveau produit fees si existant (car c un produit obligatoir)
                        this.removeFeesProducts()
                    }else if(prodFees == null){
                        //si plus de produit fees au court du temp je le supprime ou je la joute si pas de produit dans le panier
                        this.removeFeesProducts()
                    }

                }, this)
            });
        } else {
            this.cart = this.processCart(CartJS.cart);
            $d.resolve();
        }
        return $d;
    },
    hasFieldFilterChanged:function(datas){

        if(!datas || _.isEmpty(datas) ){return false;}
        var attributesNew = {};
        var attributesOld = {};
        for(var f in datas) {
            var k = this.publicFilters[f] || '_' + f;
            attributesNew[k] = datas[f];
        }
        attributesNew = this.prepareAttributes(attributesNew)

        attributesOld = _.merge({},TT.cart.attributes)
        delete(attributesOld["origin"])
        delete(attributesOld["_submit"])

        return JSON.stringify(attributesOld)!==JSON.stringify(attributesNew);
    },
    onFilterChanged: function (event, name, data) {
        console.log({data})
        data = data || {};
        var isValid = this.validateFilters(data);
        if(!!data && this.hasFieldFilterChanged(data) ){
            this.emit('filtersChanged',data);
        }
        console.log({data , isValid})
        if(data.submit && isValid) {
            /*CartJS.clear({
                success: _.bind(function () {
                    this.setFiltersAttributes(data);
                }, this)
            });*/
            this.setFiltersAttributes(data);
        } else {
            this.emit('filtersInvalidated');
        }

        this.emit('onFilterChanged',data);
    },
    getEnv: function (complete) {
        // Si complete peut retourner "TTP Michelin"
        return complete ? 'TTP' : this.originCart;
    },
    getProduct: function (variant_id) {
        if(!this.cart.items){
            return null
        }
        return _.first(_.filter(this.cart.items, (el)=>el.id === parseInt(variant_id)));
    },
    getProductLineNumber: function (variant_id) {
        return _.findIndex(this.cart.items, {variant_id: parseInt(variant_id)});
    },
    getVendor:function(cart){
        if(!cart){
            cart = this.processCart(CartJS.cart);
        }
        var list_vendor = _.uniq(cart.items.map((el)=>el.vendor))
        list_vendor = list_vendor.filter((vendor)=>vendor!==this._.vendorBonCadeau)
        return (!!cart.items)?list_vendor:[]
    },
    isMultiVendor(){
        var vendors = this.getVendor();
        //ne pas compter le vendor des prduits de bon de cadeau car il sont autoriser de les vendres ensemble
        vendors=   vendors.filter((vendor)=>vendor !== this._.vendorBonCadeau)
        //console.log(vendors)
        return vendors.length > 1
    },

    getProductInterval: function (variant_id) {
        if(window.ttpListProducts) {
            var item = _.find(ttpListProducts.products, {variantId: variant_id});
            if(item && item.quantity_interval) { return item.quantity_interval }
        }
        return [];
    },
    getCountProducts() {
        var count = 0;
        _.each(TT.cart.items, function (item) {
            if(item.product_type !== 'Livraison') {
                count += item.quantity;
            }
        });
        return count;
    },
    getQuantityForChange: function (product) {
        //   console.log({method:"TT.getQuantityForChange",product})
        var targetQuantity = parseInt(product.quantity);
        if(targetQuantity===0){
            return targetQuantity
        }
        //gestion du produit maximum a commander par jour
        if(!!product.properties && !!product.properties._maxperday && product.properties._maxperday!==-1){
            var qtyMax = parseInt(product.properties._maxperday)
            if (!!qtyMax && qtyMax < targetQuantity) {
                targetQuantity = qtyMax;
            }
        }

        if(!!product.properties && !!product.properties._interval){
            var originQuantity =  parseInt(product.properties._originQuantity)
            var interval = product.properties._interval;
            if(interval[1]) {
                if(targetQuantity < originQuantity) {
                    if(targetQuantity < interval[0]) { targetQuantity = 0; }
                    else if(targetQuantity > interval[1]) { targetQuantity = interval[1]; }
                } else {
                    if(targetQuantity < interval[0]) { targetQuantity = interval[0]; }
                    else if(targetQuantity > interval[1]) { targetQuantity = interval[1]; }
                }
            }
        }
        return targetQuantity;
    },
    isExistItemById:function(variantId){
        //   /!\ ne pas elever "._originQuantity !== 0" car c utiliser pour initliser tous les produits TT si changer le filtre
        return !!this.bufferCart[variantId] && this.bufferCart[variantId].properties._originQuantity !== 0
    },
    isExistCartItemById:function(variantId){
        return !!TT.cart.items.filter((el)=>el.id===parseInt(variantId)).length
    },
    _onProductQuantityChange: function (data) {

        if(data.quantity === undefined || !data.variant_id) { return; }
        console.log({method:"_onProductQuantityChange",bufferCart: this.bufferCart,data})
        //chercher si item exist dans le panier
        if(this.countFees == 0){
            this.addFeesProduct();
        }

        var itemCart = this.cart.items[this.getProductLineNumber(data.variant_id)] || {};
        data.quantity = this.getQuantityForChange(data);
        this.emit('refreshQty', data);

        //bloquer les boutons plus et moins

        if(!itemCart || parseInt(itemCart.quantity) !== parseInt(data.quantity) && (!!itemCart.variant_id || data.quantity > 0)) {
            var toUpdate = {};
            toUpdate[data.variant_id] = data.quantity;
            if(data.quantity === 0) {
                data.toRemove = true;
                this.emit('itemCartUpdated', data);
            }

            if(!this.isExistCartItemById(data.variant_id) && data.quantity !== 0){
                data.properties._originQuantity = 0
            }
            this.bufferCart = Object.assign(this.bufferCart || {}, {[data.variant_id]:data});

            //Verfifier si le produit existe dans le panier ou que la demander est de le supprimer
            if(this.isExistItemById(parseInt(data.variant_id)) || data.quantity === 0 ){
                console.log({method:"CartJS TRUE isExistItemById",data,properties: data.properties})
                CartJS.updateItemQuantitiesById(toUpdate, {
                    success: _.bind(function (cart) {
                        console.log({method:"CartJS properties",cart})
                        this.cart = this.processCart(cart);
                        //  a eviter boucle
                        this.emit('itemCartUpdated', data);
                        this.emit('openBtnQty', data);
                        this.renderBubbleQty()
                        if(this.countProductTT === 0 ){
                            this.emit('productEmpty', data);
                            //init le produit de livraison si plus de produit TT
                            if(this.deliveryType === 'delivery') {
                                this.adaptDelivery()
                            }
                        }

                        this.adaptFees();

                    }, this)
                });
            }
            else{
                //ajout de la date de creation du produit
                data.properties._createdAt=new Date()
                //si le produit n'existe pas l'ajouter par la nouvelle method addTTItem
                // qui est une fusion de la method addItem et getCart
                //TODO verifier si c un produit _is_tt et que le filtre a une data et heure
                console.log({method:"CartJS FALSE isExistItemById",data,properties: data.properties})
                CartJS.addTTItem(
                    parseInt(data.variant_id),
                    parseInt(data.quantity) ,
                    data.properties || null,
                    {
                        success:_.bind(function(cart){
                            console.log({method:"CartJS properties",cart})
                            // console.log({msg:"addTTItem",cart})
                            this.cart = this.processCart(cart);
                            //  a eviter boucle
                            this.emit('itemCartUpdated', data);
                            this.emit('openBtnQty', data);

                            this.renderBubbleQty()

                            if(this.countProductTT === 0 ){
                                this.emit('productEmpty', data);
                                //init le produit de livraison si plus de produit TT
                                if(this.deliveryType === 'delivery') {
                                    this.adaptDelivery()
                                }
                            }

                            this.adaptFees();
                        } , this)
                    }
                );
            }
        }

        //TODO ajouter un emit pour changer l affichage des different composant

    },
    renderBubbleQty:function(){
      //var total = TT.countQty < 10 ? TT.countQty : '+9'
       $("#CartBubble").html(TT.countQty)
    },
    onChange_ProdQtyCart:function (evt, name, data) {
        this._onProductQuantityChange(data);
    },
    onChange_ProdQtyList: function (evt, name, data) {
        this._onProductQuantityChange(data);
    },
    onAdditionalInfosChange: function (evt, name, data) {
        this.setAttributes({'Mes informations complementaires': data.split(',').join('__')})
    },
    onchangeDelivery:function(evt,name,data){

        this.removeDeliveryProducts()
        this.setAttributes(data)
        this.addDeliveryProduct()
            .then(_.bind(function () {
                //  console.log("onchangeDelivery => changeDelivery")
                this.emit("changeDelivery")
            }, this));
    },
    bindEvents: function() {
        $(document).off('cart.ready').on('cart.ready', _.bind(this.onCartJSReady, this))

            .off('SCFilterMenu.changedDataFilter').on('SCFilterMenu.changedDataFilter', _.bind(this.onFilterChanged, this))
            .off('SCFilterModal.changedDataFilter').on('SCFilterModal.changedDataFilter', _.bind(this.onFilterChanged, this))

            .off('SCCartPanel.changeProductQuantity').on('SCCartPanel.changeProductQuantity', _.debounce(_.bind(this.onChange_ProdQtyCart,this), this._.debounceTimeValue))
            .off('SCLayoutCollections.changeProductQuantity').on('SCLayoutCollections.changeProductQuantity', _.debounce(_.bind(this.onChange_ProdQtyList,this), this._.debounceTimeValue))
            .off('SCLayoutCollection.changeProductQuantity').on('SCLayoutCollection.changeProductQuantity', _.debounce(_.bind(this.onChange_ProdQtyList,this), this._.debounceTimeValue))
            .off('SCLayoutDetail.changeProductQuantity').on('SCLayoutDetail.changeProductQuantity', _.debounce(_.bind(this.onChange_ProdQtyList,this), this._.debounceTimeValue))

            .off('SCCartPanel.changeDelivery').on('SCCartPanel.changeDelivery', _.debounce(_.bind(this.onchangeDelivery,this), this._.debounceTimeValue))
            .off('SCCartPanel.changeAdditionalInfos').on('SCCartPanel.changeAdditionalInfos', _.debounce(_.bind(this.onAdditionalInfosChange, this), this._.debounceTimeValue))
    },
    onReady: function () {
        this.cart = this.processCart(CartJS.cart);

        //console.log({delCart: !this.DateValidCart ,DateDiffCart:this.DateDiffCart})
        if(!this.DateValidCart && !!this.DateDiffCart){
            this.clearCart();
            location.reload();
        }
        this.ready = true;
        window.TT = window.TT || this;

        this.adaptFees();
        this.adaptDelivery().then(_.bind(function () {
            this.emit('ready', this);
        }, this))

        if(this.validateFilterCartAttributes()) {
            this.emit('filtersValidated', this.cart.attributes);
        }
        this.renderBubbleQty()
    },
    onCartJSReady: function () {
        this.onReady();
    },
    init: function () {
        this.bindEvents();
        var self = this;
        console.log("%cSTART INIT PART.controller","background:cyan;color:#333")
        CartJS.init(self.cart, {
            moneyFormat: self.moneyFormat,
            moneyWithCurrencyFormat: self.moneyWithCurrencyFormat,
            rivetsModels: {
                customer: self.customer
            }
        });

    }
};
/*
$('.modal--quick-shop')
    .on('mouseup', function(e){
        e.preventDefault();
        _TOOLS.updateStyleModalForBarUrlMobile()
    });
*/
/*

function testSize(){

    if(window.innerHeight === document.documentElement.clientHeight){
        $(".site-nav__icons").css("border","1px solid green")
    }else{
        $(".site-nav__icons").css("border","1px solid red")
    }
}


$(".site-nav__icons").css("border","1px solid red")
*/
console.log("%cRENDER PART.controller","background:yellow;color:#333")