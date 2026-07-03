function SCFilterMenu(disabledDates,maxOrderHour,initMinDate,ecartDay,ecartHour,isWeekends) {
    // console.log({msg:'SCFilterMenu',maxOrderHour,initMinDate,ecartDay,ecartHour,isWeekends})
    this.maxOrderHour =maxOrderHour;
    this.initMinDate =initMinDate;
    this.ecartDay =ecartDay;
    this.ecartHour =ecartHour;
    this.isWeekends =isWeekends;
    this.disabledDates =disabledDates;
    this.dispoDay={};

    this.nowDate = new Date();
    //  this.nowDate = _TOOLS.strToDate("10/05/2022","14:00");
}

SCFilterMenu.prototype = {
    _: {
        selectors: {
            formFilter:"#delivery_form",
            datePicker:"#datepicker",
            pickup_popup:"#popup_type_delivery",


            stepDelivery :".js-popup-order-label",
            stepDate:".js-step-date",
            stepHour:".js-step-hour",

            filtre_resume:".js-filtre-resume",
            filtre_alert:".js-filtre-alert",
            filtre_alert_overlay:".js-alert-overlay",

            filtre_overlay:".js-filtre-overlay",

            filtre_menu:".js-filtre-menu",

            resume_text:".js-resume-text",
            btnTypeDelivery:  ".js-order-value",
            selectTypeDelivery:  ".js-order-mobile-value",
            order:"#order"
        },
        messages:{
            notTypeDelivery:"Veuillez choisir un mode de livraison",
            notDateDelivery:"Veuillez choisir une date"
        }
    },
    get orderText(){
        var filterHour = _TOOLS.replaceAll(this.filter.hour,":00","h")
        return "Commande <span class='lowercase'>" + this.filter.deliveryTypeString + "</span> - " +  this.filter.date + " - " +  filterHour.replace("-"," - ")
    },
    get orderTextMobile(){
        if(this.filter.deliveryType==="delivery"){
            var deliveryTypeStringMobile = "En livraison"
        }else{
            var deliveryTypeStringMobile = "&Agrave; emporter"
        }
        var filterHour = _TOOLS.replaceAll(this.filter.hour,":00","h")
        return deliveryTypeStringMobile +" - "+_TOOLS.getDateString(this.filter.date,{is_day:false})+ " - " + filterHour.replace("-","/")
        //return this.filter.date + " - " + this.filter.hour

    },
    get enDate() {
        var date = this.filter.date;
        if(!!date) {
            var split = date.split('/')
            return [split[2],split[1],split[0]].join('-')
        }
    },
    emit: function (name) {
        console.log("EMIT SCFilterMenu." + name,{arguments})
        $(document).trigger('SCFilterMenu.' + name, arguments);
    },

    getDispoDate:function(date){

        var day = date.getDay()
        //,m = date.getMonth(),d = date.getDate(),y = date.getFullYear();
        // var currentDate = (d<=9?"0":"") +d + '/'+ (m + 1<=9?"0":"") + (m + 1) + '/' + y ;
        var currentDate = _TOOLS.dateToStr(date);

        // console.log({currentDate,day,m,d,y,date,diff:_TOOLS.dayDiff(_TOOLS.dateToStr(new Date()),currentDate)})
        // enlever les dates avant now car iphone on peux cliquer dessus
        var nbJourIntervalAutoriser = _TOOLS.dayDiff(_TOOLS.dateToStr(new Date()),currentDate) - this.minDate

        if(nbJourIntervalAutoriser < -1){
            return [false];
        }

        //enlever les date de fermeture
        if(this.disabledDates.length > 0){
            if(_TOOLS.isIntervalDate(currentDate,this.disabledDates.join(','))){
                return [false];
            }
        }
        //refuser le weekend
        if(!this.isWeekends && [6,0].includes(parseInt(day))){
            return [false];
        }
        //  console.log({currentDate,minDate:this.minDate})
        //afficher que les jours accepter du chef
        return [this.dispoDay.includes(parseInt(day))];

    },
    toggle:function (element, toggle, isflex) {

        if(toggle) {
            if(!!isflex) {
                $(element).css('display', "flex")
            } else {
                $(element).css('display', "block")
            }
        } else {
            $(element).css('display', "none")
        }
    },
    clearInput: function(input) {


        if(input == "#datepicker" || input == "#datepickerMobile"){

            if( input == "#datepickerMobile"){
               // console.trace({method:"clearInput"})
                // $("#datepickerMobile").val(_TOOLS.dateToStr(dateNow));
                $("#datepickerMobile").val("");
                this.dateClearableOnMobile()
                // $("#datepickerMobile").val("");
                //    $("#datepickerMobile").val(_TOOLS.strFRToStrUS(_TOOLS.dateToStr(_TOOLS.DATE_NOW)));
                // $("#datepicker__label").html("");
            }else{
                $("#datepicker").val("");
            }
            $("#datepicker__label").html($("#datepicker__label").attr("data-placeholder"));
        }else{
            $(input).val("");
        }
    },
    resume:function() {
        if(this.pickup == true && this.date == true && this.hours == true) {
            $(".js-resume-text").html(this.orderText);
            $(".js-resume-text-mobile").html(this.orderTextMobile);
            this.toggle(this._.selectors.filtre_overlay, false);
            this.toggle(this._.selectors.filtre_menu, false);
            this.toggle(this._.selectors.filtre_resume, true,true);
        }
    },

    initOptions:function(){
        this.pickup = false;
        this.date = false;
        this.hours = false;

        this.minDate = this.initMinDate;
        //si vendredi et superieur a maxOrderHour heures
        if ( this.nowDate.getDay() === 5 &&  this.nowDate.getHours() >  this.maxOrderHour  ) {
            this.minDate = 3 + this.initMinDate;//nombre de jour autoriser apres le jour actuel
        }
        else if( this.nowDate.getDay() == 6 ){minDate=2+this.initMinDate;}   //pour samedi
        else if( this.nowDate.getDay() == 0){minDate=1+this.initMinDate;}//pour dimanche
        else if(this.nowDate.getHours() >  this.maxOrderHour ) {
            //si pour nimporte quel jour apres heur max il passe au jour d apres
            this.minDate=1+this.initMinDate;
        }
    },
    initFilterWithCart:function(){
        this.filter = {}
        this.filter.deliveryType = TT.cart.attributes._deliveryType || undefined
        this.filter.deliveryTypeString = TT.cart.attributes._deliveryTypeString || undefined
        this.filter.date = TT.cart.attributes.Date || undefined
        this.filter.hour = TT.cart.attributes.Heure || undefined
        this.renderHours()

        if(TT.validateFilterCartAttributes()){
            $(this._.selectors.order).text(this.filter._deliveryTypeString);
            $(this._.selectors.order).css("opacity","1");
            $("#datepicker").val(this.filter.date)
            $("#datepickerMobile").val(this.filter.date.split('/').reverse().join('-'))

            var filterHour = _TOOLS.replaceAll(this.filter.hour,":00","h")
            $("#delivery_hour").val(filterHour.replace("-"," - "))

            this.pickup = true;
            this.date = true;
            this.hours = true;
            this.resume()
        }
    },
    clearForm:function(){
        this.filter = {}
        $(this._.selectors.order).text("Livrée/Emportée");
        $(this._.selectors.order).css("opacity",".4");
        $("#datepicker").val("")
        $("#datepickerMobile").val("")
        this.dateClearableOnMobile()
        $("#delivery_hour").val("")

        $("#datepicker__label").html($("#datepicker__label").attr("data-placeholder"));

    },
    init:function(){
        this.isPageCacheFilter = $(".js-sub_delivery_nav").attr("data-page")==="index";

        console.log("%cSTART FILTRE MENU","background:cyan;color:#333")
        //recuperer les informatrions de la section global_hours

        $('#timerContainer').html(filtre_hours_template);
        $('#timerSelectContainer').html(filtre_hours_template_select);

        this.initOptions()
        this.initFilterWithCart();

        this.bindEvents()
    },
    activeFields:function(stepFilter){
        //afficher etat des champ en fonction des variable ajouter
        $(this._.selectors.datePicker).attr("disabled","disabled")
        $("#delivery_hour").attr("disabled","disabled")
        if(!!this.filter.deliveryType){
            $(this._.selectors.datePicker).removeAttr("disabled")
            if(!!this.filter.date){
                $("#delivery_hour").removeAttr("disabled")
            }
        }

        if(stepFilter === 1){
            $(this._.selectors.pickup_popup).show();
            $('#timerContainer').hide();

            $(this._.selectors.stepDelivery).addClass('active');
            $(this._.selectors.stepDate).removeClass('active');
            $(this._.selectors.stepHour).removeClass('active');

        }else if(stepFilter === 2){
            $(this._.selectors.pickup_popup).hide();
            $('#timerContainer').hide();

            $(this._.selectors.stepDelivery).removeClass('active');
            $(this._.selectors.stepDate).addClass('active');
            $(this._.selectors.stepHour).removeClass('active');

        }else if(stepFilter === 3){
            $(this._.selectors.pickup_popup).hide();

            $(this._.selectors.stepDelivery).removeClass('active');
            $(this._.selectors.stepDate).removeClass('active');
            $(this._.selectors.stepHour).addClass('active');

        }else{
            $(this._.selectors.pickup_popup).hide();
            $('#timerContainer').hide();
            if( this.isPageCacheFilter && !TT.validateFilterCartAttributes()){
                // $(".js-sub_delivery_nav").hide();
                $(".js-sub_delivery_nav").addClass("hidden");
            }
            $(this._.selectors.stepDelivery).removeClass('active');
            $(this._.selectors.stepDate).removeClass('active');
            $(this._.selectors.stepHour).removeClass('active');

        }

    },
    toggleFiltreOverlay:function(){
        var isOverlay =  $(this._.selectors.filtre_overlay).is(":visible")
        this.toggle(this._.selectors.filtre_overlay, !isOverlay);
        if( this.isPageCacheFilter && !TT.validateFilterCartAttributes()){

            $(".js-sub_delivery_nav").addClass("hidden");

        }
        //si pop type delivery visible l effacer
        if(isOverlay) {
            this.activeFields(0)
        }

    },
    dateClearableOnMobile:function () {
        var dateMobileHtml =$("#field_filter_date_mobile").html()
        $("#datepickerMobile").remove()
        $("#field_filter_date_mobile").html(dateMobileHtml.trim())

       // console.log({dateMobileHtml})
    },
    /* CHECK DISPO DATE et HOUR*/
    initDayDispo:function(){
        var days = {'Dimanche':0, 'Lundi':1, 'Mardi':2, 'Mercredi':3, 'Jeudi':4, 'Vendredi':5, 'Samedi':6}
        this.disponibility = Object.values(chefsJS)[0].disponibility
        //  console.log({disponibility:this.disponibility})
        if(!this.filter.deliveryType){
            return false
        }
        //  console.log({dispo:JSON.stringify(this.disponibility)})
        this.dispoDay =   Object.keys(this.disponibility[this.filter.deliveryType]).map((el,index)=>{
            if(this.disponibility[this.filter.deliveryType][el].length>0)
                return days[el]
            // return { [el] : this.disponibility[this.filter.deliveryType][el]}
        }).filter((el)=>!!el)

    },
    disableHours:function(){
        var days = ['Dimanche', 'Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi']
        var daySearch =days[ _TOOLS.strToDate(this.filter.date).getDay()];
        //  console.log({dispo:this.disponibility[this.filter.deliveryType][daySearch]})

        if(!this.disponibility[this.filter.deliveryType] ){
            return {error:"Aucun type de livraison choisi",code:"not delivery Type"};
        }
        if( !this.disponibility[this.filter.deliveryType][daySearch]){
            return {error:"le chefs n'est pas disponible le "+daySearch+" donc pas d horaire",code:"not hours"};
        }
        console.log("check disableHours ")
        this.hoursCurrent = this.disponibility[this.filter.deliveryType][daySearch]
        $('.js-input-hour').attr("disabled","disabled")
        $('.js-select-hours option').attr("disabled","disabled")

        for(Hourcurrent in  this.hoursCurrent){
            //si le jour J verifier chaque horaire pour les afficher ou pas
            if(_TOOLS.dayDiff(_TOOLS.dateToStr(this.nowDate),this.filter.date) === 0){
                console.log("check hours pour le jour J " +this.ecartHour)

                if(this.hoursCurrent[Hourcurrent] >= (this.nowDate.getHours()+this.ecartHour) ){
                    if(this.filter.deliveryType === "pickup"){
                        $('.js-input-hour[data-time="'+this.hoursCurrent[Hourcurrent]+':00"]').removeAttr("disabled")
                        $('.js-select-hours option[data-time="'+this.hoursCurrent[Hourcurrent]+':00"]').removeAttr("disabled")

                    }else{
                        $('.js-input-hour[data-time="'+(parseInt(this.hoursCurrent[Hourcurrent])-1)+':00-'+(parseInt(this.hoursCurrent[Hourcurrent])+1)+':00"]').removeAttr("disabled")
                        $('.js-select-hours option[data-time="'+(parseInt(this.hoursCurrent[Hourcurrent])-1)+':00-'+(parseInt(this.hoursCurrent[Hourcurrent])+1)+':00"]').removeAttr("disabled")
                    }
                }
            }else{
                console.log("check hours pour autre jour")
                if(this.filter.deliveryType === "pickup"){
                    $('.js-input-hour[data-time="'+this.hoursCurrent[Hourcurrent]+':00"]').removeAttr("disabled")
                    $('.js-select-hours option[data-time="'+this.hoursCurrent[Hourcurrent]+':00"]').removeAttr("disabled")

                }else{
                    $('.js-input-hour[data-time="'+(parseInt(this.hoursCurrent[Hourcurrent])-1)+':00-'+(parseInt(this.hoursCurrent[Hourcurrent])+1)+':00"]').removeAttr("disabled")
                    $('.js-select-hours option[data-time="'+(parseInt(this.hoursCurrent[Hourcurrent])-1)+':00-'+(parseInt(this.hoursCurrent[Hourcurrent])+1)+':00"]').removeAttr("disabled")

                }
            }
        }
        return true;
    },

    /* ETAPE DELIVERY TYPE */
    toggleStepDelivery:function(evt){
        // console.trace({evt})
        if(  this.isPageCacheFilter){
            $(".js-sub_delivery_nav").removeClass("hidden");
        }
        if($(this._.selectors.pickup_popup).is(":hidden")){
            this.toggle(this._.selectors.filtre_overlay, true);
            this.activeFields(1)
            $(this._.selectors.pickup_popup).show();
        }else{
            this.toggle(this._.selectors.filtre_overlay, false);
            this.activeFields(0)
            $(this._.selectors.pickup_popup).hide();
        }
    },

    renderHours:function(){
        $('#timerContainer').html(filtre_hours_template);
        $('#timerSelectContainer').html(filtre_hours_template_select);

        $("#timerContainer .container-hours").append('' +
            '<div class="js-msg_notTypeDelivery">'+this._.messages.notTypeDelivery+'</div>' +
            '<div class="js-msg_notDateDelivery">'+this._.messages.notDateDelivery+'</div>')

        $(".js-hour-delivery").hide()
        $(".js-hour-pickup").hide()
        $(".js-hour-title").hide()

        if(!!this.filter.deliveryType && !!this.filter.date){
            //affichage des titre
            var typesHour = ["matin","midi","soir"]
            for(key in typesHour){
                if($(".js-hour-delivery-"+typesHour[key]).length>0){
                    $(".js-hour-title-"+typesHour[key]).show()
                }else{
                    $(".js-hour-title-"+typesHour[key]).hide()
                }
            }
            //affichage des houraires
            if( this.filter.deliveryType === "delivery"){
                $(".js-hour-delivery").show()
            }
            if( this.filter.deliveryType === "pickup"){
                $(".js-hour-pickup").show()
            }

            $(".js-hour-title").show()
            $(".js-msg_notTypeDelivery").hide();
            $(".js-msg_notDateDelivery").hide();
            $('#timerContainer').toggleClass('selected-pickup', this.filter.deliveryType === 'pickup')

        }else{
            if(!!this.filter.deliveryType ){
                $(".js-msg_notTypeDelivery").hide();
                if(!!this.filter.date ){
                    $(".js-msg_notDateDelivery").hide();
                }else{
                    $(".js-msg_notDateDelivery").show()
                }
            }else{
                $(".js-msg_notTypeDelivery").show()
                $(".js-msg_notDateDelivery").hide();
            }
        }


    },

    onTypeDelivery:function(evt){
        this.filter={}
        this.filter.deliveryType =$(evt.currentTarget).attr("data-type")
        this.filter.deliveryTypeString = $(evt.currentTarget).find('span').text()
        $(this._.selectors.order).text(  $(evt.currentTarget).find('span').text());
        $(this._.selectors.datePicker).datepicker(
            {
                minDate: this.minDate,
                showAnim: 'drop',
                beforeShow: function( input, inst){
                    $(inst.dpDiv).addClass('datepicker_filter notranslate');
                },
                beforeShowDay: _.bind(this.getDispoDate,this),
                onShow : this.onClickInputDate
            });

        //fr- en - es
        let langPage = $("html").attr("lang")
        console.log({ msg:"onClickInputDate", lang: $("html").attr("lang")})
        if(!this.isLangFr()){
           $.datepicker.setDefaults( $.datepicker.regional[ "en" ] )
        }

        this.clearInput("#datepicker");
        this.clearInput("#datepickerMobile");

        this.initDayDispo()
        $(this._.selectors.datePicker).datepicker(  { beforeShowDay:_.bind(this.getDispoDate,this)});
        $(this._.selectors.datePicker).datepicker("show").click()

        this.renderHours()

        this.pickup = true;
        this.date = false;
        this.hours = false;

    },
    onTypeDeliveryMobile:function (evt){
        this.filter={}
        var valueSelected =  $(evt.currentTarget).val()
        valueSelected = valueSelected.split("|")
        this.filter.deliveryType= valueSelected[0];
        this.filter.deliveryTypeString = valueSelected[1];
        this.renderHours()

        //   $( "#datepicker" ).datepicker().datepicker("show").click()
        // $("#datepickerMobile").focus(); // obliger de l'enlever pour cause de bug sur iphone 13 qui affiche et eteind rapidement
        this.clearInput("#datepicker");
        this.clearInput("#datepickerMobile");

        //   $(this._.selectors.order).css("opacity","1");
        this.pickup = true;
        this.date = false;
        this.hours = false;
    },
    isLangFr:function (){
       let langPage = $("html").attr("lang")
       return (langPage == "fr")
    },
    /* ETAPE DATEPICKER */
    onClickInputDate:function(){
        this.initDayDispo()
        // Calendar Manager //
        console.trace({method:"onClickInputDate",arguments})
        this.activeFields(2)
        this.toggle(this._.selectors.filtre_overlay, true);
    },
    onChangeInputDate:function(){

        $("#datepickerMobile").focus();
        var dateMobile = $("#datepickerMobile").val()
        var dateDesktop = $("#datepicker").val()
        $("#datepickerMobile").val("")
        this.clearInput("#delivery_hour");
        if(dateMobile !== "" ||  dateDesktop !== "" ){
            $("#datepicker__label").html("");
        }else{
            $("#datepicker__label").html($("#datepicker__label").attr("data-placeholder"));
        }
        //si c en Anglais changer le mois et le jour
        if(!this.isLangFr()){
            let dateEnDesktop = dateDesktop.split("/")
            //en 04/27/2023 -> fr 27/04/2023
            dateDesktop =  dateEnDesktop[1]+"/"+dateEnDesktop[0]+"/"+dateEnDesktop[2]
        }

        this.filter.date= $("html").hasClass("supports-mobile") ? dateMobile.split("-").reverse().join("/") : dateDesktop ;

        this.activeFields(3)

        $("#datepickerMobile").val(this.filter.date.split('/').reverse().join('-'))

        // $("#datepicker").val( this.filter.date)  //enlever car empecher de changer la date

        //init les informations accpeter par le chef
        this.initDayDispo()

        //recuperer la disponiblité en fonction de la date utiliser
        var disHours = this.getDispoDate(_TOOLS.strToDate( this.filter.date))
              console.log({disHours,
                  dateDesktop :  this.filter.date ,
                  strToDate:_TOOLS.strToDate( this.filter.date)})
        //console.trace({dateMobile,dateDesktop,disHours})
        if(!!disHours[0]){
            // afficher le rendu du select
            this.renderHours()
            //activer ou desacticer les heures en fonction de l heure choisi
            this.disableHours()
            $(".js-step-hour").find("input").click();

            $(".chef_indispo").remove()

        }else {
            $(".js-select-hours").hide()
            $(".chef_indispo").remove()
            $("body").append($(".templateChefIndispo").html())
            $("#datepickerMobile").blur()
        }

        this.date = true;
        this.hours = false;

    },

    /* ETAPE HOUR */

    onInputHour:function(){
        this.toggle(this._.selectors.filtre_overlay, true);
        $(this._.selectors.pickup_popup).hide();

        this.activeFields(3);
        $('#timerContainer').toggle();
    },
    onClickSelectHour:function(evt){
        evt.preventDefault()
        this.activeFields(3)
        $(this._.selectors.pickup_popup).hide();
        this.hours = true;
        var dataTime = $(evt.currentTarget).attr("data-time");
        if(!!dataTime){
            //  console.log({dataTime})
            this.filter.hour = _TOOLS.replaceAll(_TOOLS.replaceAll(dataTime,"h",":00")," ","");
            //  this.filter.hour =dataTime.replaceAll(" ","").replaceAll("h",":00");
        }
        console.log("%cRun onClickSelectHour","color:blue")
        this.toggle(this._.selectors.filtre_overlay, false);
        this.resume();
        this.filter.submit = true
        this.filter.createAt = window._TOOLS.DATE_NOW;
        this.emit("changedDataFilter",this.filter)
    },
    onChangeSelectHourMobile:function(evt){
        this.hours = true;
        this.filter.hour = $(evt.currentTarget).val()
        console.log("%cRun onClickSelectHour","color:blue")
        this.toggle(this._.selectors.filtre_overlay, false);
        //todo verifier si tous les champs bien rempli et pas d erreur
        this.resume();
        $("#delivery_form").submit();
        this.filter.submit = true
        this.filter.createAt = window._TOOLS.DATE_NOW;
        this.emit("changedDataFilter",this.filter)
    },

    closePopupChefIndispo(){
        $(".chef_indispo").remove();
        $("#datepickerMobile").focus();
    },

    onOpenPopupFilter:function(){
        console.log("%cRun onOpenPopupFilter","color:red")
        this.toggle(this._.selectors.filtre_alert_overlay, true);
        this.toggle(this._.selectors.filtre_alert, true);
    },
    onClosePopupFilter:function(){
        console.log("%cRun onClosePopupFilter","color:red")
        this.toggle(this._.selectors.filtre_alert_overlay, false);
        this.toggle(this._.selectors.filtre_alert, false);
    },
    onUpdatePopupFilter:function(evt){

        console.log("%cRun onUpdatePopupFilter","background:red;color:white")
        TT.clearTTCart()
        this.date = false;
        this.pickup = false;
        this.hours = false;
        this.toggle(this._.selectors.filtre_alert_overlay, false);
        this.toggle(this._.selectors.filtre_alert, false);
        this.toggle(this._.selectors.filtre_resume, false);
        this.toggle(this._.selectors.filtre_menu, true, true);


        if( this.isPageCacheFilter){
            $(".js-sub_delivery_nav").addClass("hidden");
        }

        $(".js-cart-product").removeClass("opacityProd");

        this.filter={}
        $(".js-filter_chefs").prop("checked", false);
        $(".js-order-mobile-value").val("")
        this.renderHours()
        this.toggleStepDelivery(evt)


    },

    refresh:function(){
        $(".js-sub_delivery_nav").removeClass("hidden");
        this.initFilterWithCart()
    },

    bindEvents: function () {
        //----les actionneurs
        $("body")
            .off("click.ChefIndispo").on("click.ChefIndispo",".js-btn_chef_indispo, .js-order-mobile-value option, #datepickerMobile, .js-filtre-overlay",_.bind(this.closePopupChefIndispo, this))

            //ouvrir la popup delivery type
            .off("click.toggleStepDelivery").on("click.toggleStepDelivery",this._.selectors.stepDelivery, _.bind(this.toggleStepDelivery, this))
            .off("click.openSelectDelivery").on("click.openSelectDelivery",".js-open-select-delivery", _.bind(this.toggleStepDelivery, this))

            .off("click.filtre_overlay").on("click.filtre_overlay",this._.selectors.filtre_overlay, _.bind(this.toggleFiltreOverlay, this))

            .off("click.typeDelivery").on("click.typeDelivery",this._.selectors.btnTypeDelivery, _.bind(this.onTypeDelivery, this))
            .off("change.typeDeliveryMobile").on("change.typeDeliveryMobile",this._.selectors.selectTypeDelivery, _.bind(this.onTypeDeliveryMobile, this))

            .off("click.inputDate").on("click.inputDate",".js-step-date",  _.bind(this.onClickInputDate, this))
            .off("change.inputDate").on("change.inputDate","input#datepicker, input#datepickerMobile",  _.bind(this.onChangeInputDate, this))


            .off("click.openHour").on("click.openHour","#delivery_hour", _.bind(this.onInputHour, this))
            .off("click.selectHour").on("click.selectHour",".js-input-hour", _.bind(this.onClickSelectHour, this))
            .off("submit.formFilter").on("submit.formFilter",this._.selectors.formFilter, _.bind(this.onClickSelectHour, this))

            .off("change.ChangeSelectHourMobile").on("change.ChangeSelectHourMobile",".js-select-hours", _.bind(this.onChangeSelectHourMobile, this))

            .off("click.BtnUpdateFilter").on("click.BtnUpdateFilter",".js-resume-button", _.bind(this.onOpenPopupFilter, this))
            .off("click.ShadowPopup").on("click.ShadowPopup",this._.selectors.filtre_alert_overlay, _.bind(this.onClosePopupFilter, this))
            .off("click.ShadowPopupCancel").on("click.ShadowPopupCancel",".js-button-cancel", _.bind(this.onClosePopupFilter, this))
            .off("click.ShadowPopupUpdate").on("click.ShadowPopupUpdate",".js-button-modify", _.bind(this.onUpdatePopupFilter, this))

        //----les écouteurs
        $(document)
            .off("TT.clearCart").on('TT.clearCart',_.debounce( _.bind(this.clearForm, this), TT._.debounceTimeValue))
            .off("TT.removeTTProducts") .on('TT.removeTTProducts',_.debounce( _.bind(this.clearForm, this), TT._.debounceTimeValue))
            .off("TT.onFilterChanged") .on('TT.onFilterChanged',_.debounce( _.bind(this.refresh, this), TT._.debounceTimeValue))


    }
};

function blink(selector) {
    var el = $(selector)
    el.removeClass("blink")
    setTimeout(function() {
        el.addClass("blink")
    }, 10);
}
