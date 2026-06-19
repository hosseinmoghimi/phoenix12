function PARTCartPanel() {
    if(window.TT && TT.ready) {
        this.init();
    } else {
        $(document).off('TT.ready.initAutocomplete').on('TT.ready.initAutocomplete', _.bind(function () {
            $(document).off('TT.ready.initAutocomplete');
            this.init();
        }, this))
    }
}

PARTCartPanel.prototype = {
    _: {
        selectors: {
            //========Selectors CartForm
            form: '#CartDrawerForm',
            itemProduct:'.cart__item',
            products: '[data-products]',
            qtySelector: '.js-qty__wrapper',
            discounts: '[data-discounts]',
            savings: '[data-savings]',
            productsContainer: '.js-cart-product-container',


            htTotal: '[data-ht]',
            tvaTotal: '[data-vat]',
            fees: '[data-fees]',
            subTotal: '[data-subtotal]',
            isTT: '[data-istt="true"]',
            isNotTT: '[data-istt="false"]',

            cartBubble: '#CartBubble',
            cartNote: '[name="note"]',
            termsCheckbox: '.cart__terms-checkbox',
            checkoutBtn: '.cart__checkout',
            checkoutMessageZip: '.js-msg-checkout',

            //========Drawers
            drawer: "#CartDrawer",
            close: '.js-drawer-close',
            open: '.js-drawer-open-cart' ,
            openClass: 'js-drawer-open',
            closingClass: 'js-drawer-closing',
            activeDrawer: 'drawer--is-open',
            namespace: '.drawer-cart',

            //========Zip

            cartFees:".js-cart-fees",
            priceFees:".js-price-fees",
            priceDelivery:".js-price-delivery",
            cardDelivery:".js-card-delivery",
            formZipDelivery:".js-form-zip-delivery",
            msgMissingZip: '.js-missing-zip-message',

            msgDeliveryProduct:".js-msg-delivery-product",
            priceDeliveryProduct:".js-price-delivery-product",
            totalPriceNotIsTT:".js-total-price-not_is_tt",
            totalPriceGiftCard:".js-total-price-giftcard",
            totalPriceIsTT:".js-total-price-is_tt",
            filterDateDelivery:".js-filter-date-delivery",
            inputZipDelivery:".js-input-zip-delivery",
            addBtnZipDelivery:".js-add-btn-zip-delivery",
            changeBtnZipDelivery:".js-change-btn-zip-delivery",
            errorMsgZipDelivery:".js-error-zip-delivery",

            //========cart-link header
            bubbleCartLink : 'cart-link__bubble--visible',

            //======== msg panier vide
            msgCartEmpty:".js-msg-cart-empty",

            //======== form buy
            quantityInput:".js-qty__num",
            quantityPlusButton:".js-qty__adjust--plus",
            quantityMinusButton:".js-qty__adjust--minus",

            additionalInfosInput: '.js-cart-attribute-additional-infos',

            preventEnter: '.js-prevent-enter'
        },
        classes:{
            btnLoading: 'btn--loading'
        },
        config:{
            requiresTerms: false
        },
        routeCart: window.Shopify.routes.root + "cart"
    },
    initSelector:function(){

        this.form = document.querySelector(this._.selectors.form) ;
        this.wrapper =  this.form.parentNode;
        this.location =  this.form.dataset.location;
        this.namespace = '.cart-' + this.location;
        this.products =  this.form.querySelector(this._.selectors.products);
        this.submitBtn =  this.form.querySelector(this._.selectors.checkoutBtn);

        this.discounts =  this.form.querySelector(this._.selectors.discounts);
        this.savings =  this.form.querySelector(this._.selectors.savings);

        this.htTotal =  this.form.querySelector(this._.selectors.htTotal);
        this.tvaTotal =  this.form.querySelector(this._.selectors.tvaTotal);
        this.subtotal =  this.form.querySelector(this._.selectors.subTotal);

        this.termsCheckbox = this.form.querySelector(this._.selectors.termsCheckbox);
        this.noteInput = this.form.querySelector(this._.selectors.cartNote);
    },
    emit: function (name) {
        console.log("%c→ EMIT PARTCart." + name,"background:#1e98ec;color:#FFF")
        console.log({arguments})
        $(document).trigger('PARTCart.' + name, arguments);
    },
    bindEvents: function () {
        $('body')
            .on('click', this._.selectors.close, _.bind(this.close, this))
            .on('click', this._.selectors.open, _.bind( this.open, this))

            .on('click', this._.selectors.addBtnZipDelivery, _.bind(this.addZip, this))
            .on('click', this._.selectors.changeBtnZipDelivery, _.bind(this.showFormZip, this))

            .off("blur.qtyInput").on("blur.qtyInput", this._.selectors.quantityInput, _.bind(this.onInputProductQuantity, this))
            .off("keyup.qtyInput").on("keyup.qtyInput", this._.selectors.quantityInput, _.bind(this.onInputProductQuantity, this))

            .off("click.qtyPlus").on("click.qtyPlus", this._.selectors.quantityPlusButton, _.bind(this.onPlusProductQuantity, this))
            .off("click.qtyMinus").on("click.qtyMinus", this._.selectors.quantityMinusButton, _.bind(this.onMinusProductQuantity, this))

            .off("change.additionalInfos").on("change.additionalInfos", this._.selectors.additionalInfosInput, _.bind(this.changeAdditionalInfos, this))

            .off("keyup.preventEnter").on("keyup.preventEnter", this._.selectors.preventEnter, _.bind(this.preventEnter, this))

            .off("click.missingZip").on("click.missingZip", this._.selectors.msgMissingZip, _.bind(this.onMissingZipMessageClicked, this))
            //  .off("click.checkout").on("click.checkout", "button.cart__checkout[name='checkout']",_TOOLS.redirectToCheckout)
            // .off("click.checkout").on("click.checkout", "button.cart__checkout[name='checkout']",_.bind(function(evt){this.onSubmit(evt).then(this.redirectToCheckout);}, this));
            .on('click.checkout', '#formOpenCheckout', _.bind(this.onSubmit, this));

        $(".main-content").after().on('click', _.bind(this.close, this));

        $(document)
            .on('TT.refreshQty', _.bind(this.synchronizeProductsDisplay, this))
            .on('TT.itemCartUpdated', _.bind(this.render, this))
            .on('TT.productEmpty', _.bind(this.render, this))
            .on('TT.clearCart',_.debounce( _.bind(this.render, this), TT._.debounceTimeValue))
            .on('TT.removeTTProducts',_.debounce( _.bind(this.render, this), TT._.debounceTimeValue))
            .off("TT.changeDelivery").on('TT.changeDelivery', _.bind(this.render, this))
            .off("STRIPE.notNeedDeposit").on('STRIPE.notNeedDeposit', _.bind(this.redirectToCheckout, this))
    },
    init:function(){
        //init la variable pour dire que le panel est fermé
        this.isOpen = false;
        //=== creation du panel du panier
        this.render()
        //=== listener des events
        this.bindEvents();
        //=== recuperer les selectors du panel
        this.initSelector()
    },
    onSubmit: function (evt) {
        console.log("RUN onSubmit =>checkStripeDeposit")
        evt.preventDefault();
        checkStripeDeposit().then(function () {
            document.location = '/checkout';
        });
    },
    redirectToCheckout: function(){
        console.log({arguments})
       // window.location.href = '/checkout';
        console.log("redirect window.location.href = '/checkout'")
    },
    showFormZip:function(){
        $(this._.selectors.cardDelivery).addClass("hide");
        $(this._.selectors.formZipDelivery).removeClass("hide");
    },
    hideFormZip:function(){
        $(this._.selectors.cardDelivery).removeClass("hide");
        $(this._.selectors.formZipDelivery).addClass("hide");
    },
    pickupFormZip:function(){
        $(this._.selectors.cardDelivery).addClass("hide");
        $(this._.selectors.formZipDelivery).addClass("hide");
    },
    changeAdditionalInfos: function (evt) {
        this.emit("changeAdditionalInfos", $(evt.currentTarget).val())
    },
    preventEnter: function (evt) {
        evt.preventDefault();
    },
    addZip:function(){
        //recuperer le zip pour le save ds le cartJS attribute
        var zip=$(this._.selectors.inputZipDelivery).val();
        this.emit("changeDelivery",{zip})
    },
    initZip:function(){
        // console.log("%c RUN initZip",'background:red;color:white')

        if( (!!TT.cart.attributes.zip && (!TT.cart.attributes._zone ||  TT.cart.attributes._zone === "false") ) || (TT.cart.attributes.zip !== undefined && TT.cart.attributes._zone === "false" )){
            $(this._.selectors.errorMsgZipDelivery).removeClass("hide")
        }else{
            $(this._.selectors.errorMsgZipDelivery).addClass("hide")
        }
        if(TT.cart.attributes._deliveryType === "delivery"){
            if(!!TT.cart.attributes.zip){
                $(this._.selectors.inputZipDelivery).val(TT.cart.attributes.zip);
            }
            //   console.log({attr:TT.cart.attributes})
            if( !!TT.cart.attributes.zip
                && !!TT.cart.attributes._zone
                && TT.cart.attributes._zone!=="false"
                && TT.countDelivery !== 0){
                $(this._.selectors.changeBtnZipDelivery).html(TT.cart.attributes.zip);
                this.hideFormZip()
            }else{

                this.showFormZip()
            }
        }else{
            this.pickupFormZip()
        }

    },

    getCartProducts:function(){
        var params_theme_id = (Shopify.theme.role!="cart")?"?view=api":"";
        if(!!window._isPreview) {
            params_theme_id += "&fts=0&preview_theme_id="+ Shopify.theme.id
        }
        this.cartSC = {}
        $.get(window.Shopify.routes.root + 'cart' + params_theme_id)
            .then(_.bind(function (response) {
                response = response.split('<!-- BEGIN template -->')[1] || response.split('<!-- BEGIN template -->')[0];
                response = response.split('<!-- END template -->')[0];
                this.cartSC = _.merge(this.cartSC, JSON.parse(response))
            }, this))
    },

    refresh:function (){
        this.getCartProducts()

        this.synchronizeProductsDisplay()

        if (TT.countProducts > 0) {
            $(this._.selectors.cartBubble).addClass(this._.selectors.bubbleCartLink);
            $(this._.selectors.msgCartEmpty).addClass("hide");
        }
        else {
            $(this._.selectors.cartBubble).removeClass(this._.selectors.bubbleCartLink);
            $(this._.selectors.msgCartEmpty).removeClass("hide");
        }

        if(TT.countDelivery){
            $(this._.selectors.priceDelivery)
                .html(new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'EUR' })
                    .format(parseInt(TT.priceDelivery)))
        }
        $(this._.selectors.cartFees).html("")
        if(TT.countFees){
            let priceFees = new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'EUR' })
                    .format(TT.priceFees);
            let templateFees = `<div class="cart__item-price-details cart__item-row">
                <div class="cart__item-sub">
                  <div class="cart__subtotal cart_fees_title">
                    Frais de gestion</div>
                  <div class=" cart_fees_price" data-fees>`+priceFees+`</div>
                </div>
              </div>`;
            $(this._.selectors.cartFees).html(templateFees)

        }

        //deliveryNotTTMsg variable genererique enregistrer par le customize
        $(this._.selectors.msgDeliveryProduct).html(window.deliveryNotTTMsg);
        //priceDeliveryNotTT variable genererique enregistrer par le customize
        /*
        $(this._.selectors.priceDeliveryProduct)
                 .html(new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'EUR' })
                     .format(priceDeliveryNotTT))
        */

        $(this._.selectors.priceDeliveryProduct).html("")


        $(this._.selectors.totalPriceGiftCard)
            .html(new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'EUR' })
                .format(parseInt(TT.priceGiftCard) ))

        $(this._.selectors.totalPriceNotIsTT)
            .html(new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'EUR' })
                .format(parseInt(TT.priceNotTTProduct) + parseInt(window.priceDeliveryNotTT)))

        $(this._.selectors.totalPriceIsTT)
            .html(new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'EUR' })
                .format(parseInt(TT.priceTTProduct) + parseInt(TT.priceDelivery)))

        $(this._.selectors.filterDateDelivery).html(TT.strDateDelivery)

        this.checkBtnCartCheckout()
        this.initZip()
        if (document.body.classList.contains('template-cart')) {
            if(TT.countProducts > 0){
                $(".js-cart-page-products").html($(".cart__items").html())
                $(".js-cart-page-total").html("")
                    .append($(".cart__item-price-details").html())
                    .append($(".js-btn-checkout").html())
            }else{
                $(".js-cart-page-products").html($(".js-msg-cart-empty").html())
                $(".js-cart-page-total").html("")
            }
        }
    },
    checkBtnCartCheckout: function(){
        if( TT.validateCheckoutCartAttributes() || (TT.ProductisTT.length === 0 && (TT.countProductGiftCard !== 0 || TT.ProductisNotTT.length !==0) ) ){
            $(this._.selectors.checkoutBtn).removeClass("hide")
            $(this._.selectors.checkoutMessageZip).addClass("hide")
        }else{
            $(this._.selectors.checkoutBtn).addClass("hide")
            $(this._.selectors.checkoutMessageZip).removeClass("hide")
        }
    },
    render:function(){
        this.getTemplateCartPanel().then(_.bind(this.builderTemplate,this));
    },
    getTemplateCartPanel:function(){

        console.log("%cRUN PARTCartPanel.getTemplateCartPanel","background:cyan;color:#333")
        var url = ''.concat(this._.routeCart, '?t=').concat(Date.now());

        url = url.indexOf('?') === -1 ? (url + '?view=ajax') : (url + '&view=ajax');
          // console.log({getTemplateCartPanel:url})
        return fetch(url, {credentials: 'same-origin', method: 'GET'})
            .then((response)=>response.text());
    },
    builderTemplate: function(html){
        console.log("%cRUN PARTCartPanel.builderTemplate","background:cyan;color:#333")
        var markup = this._parseProductHTML(html);
        var items = markup.items;
        var subtotal = items.dataset.cartSubtotal;
        if( TT.priceNotTTProduct>0 ){
            subtotal = parseFloat(subtotal) + (parseFloat(window.priceDeliveryNotTT || 0) * 100)
        }

        this.updateCartDiscounts(markup.discounts);

        if (TT.countProducts > 0) {
            this.wrapper.classList.remove('is-empty');
        } else {
            this.wrapper.classList.add('is-empty');
        }

        // Append item markup
        this.products.innerHTML = '';
        this.products.append(items);
        //TODO manage de la TVA
        // this.htTotal.innerHTML = this.formatPrice(subtotal);
        // this.tvaTotal.innerHTML = this.formatPrice(subtotal);
        //======TOTAUX GENERAL
        this.subtotal.innerHTML = this.formatPrice(subtotal);

        //initialiser les champs du panel
        // this.reInit();
        //refresh l animation  de la page
        if (window.AOS) { AOS.refreshHard() }
        if (Shopify && Shopify.StorefrontExpressButtons) {
            Shopify.StorefrontExpressButtons.initialize();
        }
        this.refresh()
    },
    _parseProductHTML: function(html) {
        var parser = new DOMParser();
        var doc = parser.parseFromString(html, 'text/html');
        return {
            items: doc.querySelector('.cart__items'),
            discounts: doc.querySelector('.cart__discounts')
        }
    },
    updateCartDiscounts: function(markup) {
        if (!this.discounts) {
            return;
        }
        this.discounts.innerHTML = '';
        this.discounts.append(markup);
    },

    formatPrice : function(price){

        //     return theme.Currency.formatMoney(price,theme.settings.moneyFormat)
        return new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'EUR' })
            .format(parseInt(price)/100)
    },

    //-----Manage du panel panier
    open: function(evt, returnFocusEl) {
        if (evt) {
            evt.preventDefault();
        }

        if (this.isOpen) {
            this.close(evt)
            return;
        }
        theme.NavDrawer.close()

        $(this._.selectors.open).attr('aria-expanded', 'false');

        // Without this the drawer opens, the click event bubbles up to $nodes.page which closes the drawer.
        if (evt && evt.stopPropagation) {
            evt.stopPropagation();
            // save the source of the click, we'll focus to this on close
            evt.currentTarget.setAttribute('aria-expanded', 'true');
            this.activeSource = evt.currentTarget;
            setDatalayerGTM("GTM_HEADER_PANIER",{})
        } else if (returnFocusEl) {
            returnFocusEl.setAttribute('aria-expanded', 'true');
            this.activeSource = returnFocusEl;
        }

        theme.utils.prepareTransition($(this._.selectors.drawer)[0], _.bind(function() {
            $(this._.selectors.drawer)[0].classList.add(this._.selectors.activeDrawer);
        },this));

        document.documentElement.classList.add(this._.selectors.openClass);
        this.isOpen = true;

        theme.a11y.trapFocus({
            container:$(this._.selectors.drawer)[0],
            namespace: 'drawer_focus'
        });
        $(document).trigger('THEME.panelCartOpen');
        document.dispatchEvent(new CustomEvent('drawerOpen'));
        document.dispatchEvent(new CustomEvent('drawerOpen.CartDrawer'));

    },
    close: function(evt) {
        if (!this.isOpen) {
            return;
        }

        // Do not close if click event came from inside drawer
        if (evt) {
            if (evt.target.closest('.js-drawer-close')) {
                // Do not close if using the drawer close button
            } else if (evt.target.closest('.drawer')) {
                return;
            }
        }

        // deselect any focused form elements
        document.activeElement.blur();

        theme.utils.prepareTransition($(this._.selectors.drawer)[0], _.bind(function() {
            $(this._.selectors.drawer)[0].classList.remove(this._.selectors.activeDrawer);
        },this));


        document.documentElement.classList.remove(this._.selectors.openClass);
        document.documentElement.classList.add(this._.selectors.closingClass);

        window.setTimeout(function() {
            document.documentElement.classList.remove(this._.selectors.closingClass);
            if (this.activeSource && this.activeSource.getAttribute('aria-expanded')) {
                this.activeSource.setAttribute('aria-expanded', 'false');
                this.activeSource.focus();
            }
        }.bind(this), 500);

        this.isOpen = false;

        theme.a11y.removeTrapFocus({
            container:  $(this._.selectors.drawer)[0],
            namespace: 'drawer_focus'
        });

        $(document).trigger('THEME.panelCartClose');
        //this.unbindEvents();
    },

    //--- recuperer l'interval du produit si existe
    getProductInterval: function(variantId) {
        if(!this.cartSC || !this.cartSC.products || !this.cartSC.products[variantId]){return -1}
        var quantity_interval= this.cartSC.products[variantId].quantity_interval
        if(quantity_interval===""){
            return undefined
        }
        var interval= quantity_interval.split("|");
        return [parseInt(interval[0]), parseInt(interval[1])];
    },
    getQuantityMaxperday:function(variantId){
        if(!this.cartSC || !this.cartSC.products || !this.cartSC.products[variantId]){return -1}
        var product = this.cartSC.products[variantId];

        var qtyMax = undefined
        if (product.max_per_day !== -1) {
            qtyMax = product.max_per_day - (product.kept_quantity[this.cartSC.attributes.Date]===undefined?0:product.kept_quantity[this.cartSC.attributes.Date]);
        }
        return qtyMax;
    },
    onMissingZipMessageClicked: function () {
        $(this._.selectors.productsContainer).animate({scrollTop: $(this._.selectors.productsContainer).height()})
    },
    //--- action sur les boutons pour le produits
    onInputProductQuantity: function (evt) {
        var qty = $(evt.target).val() || 0
        this.changeProductQuantity($(evt.target), qty <= 0 ? 0 : qty , "input");
    },
    onPlusProductQuantity: function (evt) {
        var $quantityInput = $(evt.target).closest(this._.selectors.itemProduct).find(this._.selectors.quantityInput);
        if(!this.bufferQtyPlus){
            this.bufferQtyPlus= parseInt($quantityInput.val() || 0) + 1
        }else{
            this.bufferQtyPlus=  this.bufferQtyPlus + 1
        }
        this.changeProductQuantity($quantityInput, this.bufferQtyPlus,"plus");
    },
    onMinusProductQuantity: function (evt) {
        //console.log("onMinusProductQuantity ->"+evt.type)
        var $quantityInput = $(evt.target).closest(this._.selectors.itemProduct).find(this._.selectors.quantityInput);
        if(!this.bufferQtyMinus){
            this.bufferQtyMinus= parseInt($quantityInput.val() || 0) - 1
        }else{
            this.bufferQtyMinus=  this.bufferQtyMinus - 1
        }
        this.changeProductQuantity($quantityInput,this.bufferQtyMinus, "minus");
    },
    changeProductQuantity: function ($input, targetQuantity, type) {
        var originQuantity    = $input.val() || 0;
        if(type !== "input"  && originQuantity === targetQuantity || targetQuantity < 0) { return; }
        var variantId    = $input.attr('data-variant');
        var tags   = $input.attr('data-tags');
        var vendor = $input.attr('data-vendor');
        originQuantity = parseInt(originQuantity);
        targetQuantity = parseInt(targetQuantity);

        var datas =  {
            variant_id: variantId,
            quantity: targetQuantity,
            vendor: vendor,
            properties: {
                _originQuantity:originQuantity,
                _maxperday: this.getQuantityMaxperday(variantId),
                _interval: this.getProductInterval(variantId),
                _vendor : vendor,
                _deposit: _.includes(tags,"_DEPOSIT"),
                _is_tt: _.includes(tags,"_is_tt"),
                _is_magic: _.includes(tags,"_CHILD_PRICE") || _.includes(tags,"_FREE_PRICE")

            }};

        var returnData = Object.assign(datas,{quantity:TT.getQuantityForChange(datas)})

        this.renderFormQty(null,null,returnData)

        $(".cart__qty-adjust").attr("disabled","disabled");
        $(".js-qty__adjust--"+type+"[data-variant='"+variantId+"']").removeAttr("disabled")

           $(".form__btn").attr("disabled","disabled");
            $(".product-row-qty-"+type+"[data-variant='"+variantId+"']").removeAttr("disabled")


        console.log("%cRUN PARTCartPanel.changeProductQuantity","background:orange;color:#333")
        this.emit('changeProductQuantity',datas);

    },

    //getter
    getProductQuantityInput: function (variant_id) {
        return $(this._.selectors.quantityInput + '[data-variant="' + variant_id + '"]');
    },
    getProductQuantityMinus: function (variant_id) {
        return $(this._.selectors.quantityMinusButton + '[data-variant="' + variant_id + '"]');
    },
    getProductQuantityPlus: function (variant_id) {
        return $(this._.selectors.quantityPlusButton + '[data-variant="' + variant_id + '"]');
    },

    synchronizeProductsDisplay: function (event, name, data) {
        console.log("%cRUN PARTCartPanel.synchronizeProductsDisplay","background:green;color:white")
        if(!!data) {
            this.renderFormQty(null,null,data);
        } else {
            _.each(TT.cart.items, _.bind(function (item) {
                if(!['Livraison','frais_de_gestion'].includes(item.product_type)) {
                    this.renderFormQty(null,null,item)
                }
            }, this));
        }
    },
    renderFormQty:function(evt,name,data){
        this.bufferQtyPlus=  undefined
        this.bufferQtyMinus=  undefined
        console.log("%cRUN PARTCartPanel.renderFormQty","background:orange;color:#333")
     //   console.log({data})
        var vid = data.variant_id
        var qty = data.quantity

        var $element_InputQty = this.getProductQuantityInput(vid)
        var $element_PlusBtn = this.getProductQuantityPlus(vid)

        $element_PlusBtn.removeClass("lock")
        var qtyMax = 1000
        //--- check la quantité en fonction du properties d un item dans le panier
        if(!!data.properties ){
            if(!!data.properties._maxperday && data.properties._maxperday!== -1 && data.properties._maxperday!== 0 && !!data.properties._interval && data.properties._maxperday!== NaN){
                qtyMax = data.properties._maxperday <= data.properties._interval[1]? data.properties._maxperday:data.properties._interval[1]
            }
            else if(!!data.properties._maxperday && data.properties._maxperday!== 0 && data.properties._maxperday!== -1){
                qtyMax = data.properties._maxperday
            }
            else if(!!data.properties._interval && !!data.properties._interval[1] && data.properties._maxperday!== NaN){
                qtyMax = data.properties._interval[1]
            }
        }else{
            console.log({method:"PARTCart.renderFormQty  pas de properties !!",data})
        }
        qtyMax=parseInt(qtyMax)

        $element_PlusBtn.removeClass("lock")
        if(qtyMax === qty){
            $element_PlusBtn.addClass("lock")
        }

        $element_InputQty.val(qty).trigger('change');

    },

}