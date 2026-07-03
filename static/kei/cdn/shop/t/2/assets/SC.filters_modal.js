if(!!SCFilterMenu) {
    function SCFilterModal(disabledDates,maxOrderHour,initMinDate,ecartDay,ecartHour,isWeekends) {
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

    SCFilterModal.prototype = {
        _: {
            selectors: {
                formFilter:".js-modal-window",
                datePicker:".js-datepicker",

                resume_text:".js-modal-resume-text",
                popup_order :".js-popup-order",
                btnTypeDelivery:  ".js-order-value",
                stepDate:".js-step-date",
                order:"#order",

                btn_pickup: '.js-mw-1__btn1',
                btn_delivery: '.js-mw-1__btn2',
                calendar: ".js-datepicker",
                btn_submit: '.js-mw-footer-btn1'

            }
        },
        emit: function (name) {
            console.log("EMIT SCFilterModal." + name, {arguments})
            $(document).trigger('SCFilterModal.' + name, arguments);
        },
        init: function () {
            console.log("%cSTART FILTRE MODAL","background:cyan;color:#333")
            this.bindEvents()
            this.render()
        },
        render: function () {
            console.log("%cSTART RENDER MODAL", "background:cyan;color:#333")
            this.initFilterWithCart()
            //  $("body").find('.modal-window').removeClass("hide")
        },
        bindEvents: function () {
            //----les actionneurs
            $("body")
                // Boutons window 1
                .off('click.btn_modal_pickup').on('click.btn_modal_pickup', this._.selectors.btn_pickup, _.bind(this.onClickBtnPickup, this))
                .off('click.btn_modal_delivery').on('click.btn_modal_delivery', this._.selectors.btn_delivery, _.bind(this.onClickBtnDelivery, this))
                //Boutons window 2
                .off('change.modal_datepicker').on('change.modal_datepicker', this._.selectors.calendar, _.bind(this.onChangeDatepicker, this))

                //Boutons window 3
                .off('click.onHourModal').on('click.onHourModal', '.js-mw-3__item',_.bind(this.onClickHour, this))

                //Boutons Submit
                .off('click.onSubmitModal').on('click.onSubmitModal', this._.selectors.btn_submit, _.bind(this.onSubmit, this))

                // Boutons rollback
                .off('click.modal-window-1-rollback').on('click.modal-window-1-rollback', '.js-mw-footer__commande',_.bind(this.onCLickRollbackStep1, this) )
                .off('click.modal-window-2-rollback').on('click.modal-window-2-rollback', '.js-mw-footer__date', _.bind(this.onCLickRollbackStep2, this))
                .off('click.modal-window-3-rollback').on('click.modal-window-3-rollback', '.js-mw-footer__hour',_.bind(this.onCLickRollbackStep3, this))

            //----les écouteurs

            $(document)
                .on('TT.clearAttributes', _.debounce(_.bind(this.onCLickRollbackStep1, this), TT._.debounceTimeValue))
                .on('TT.onFilterChanged', _.debounce(_.bind(this.render, this), TT._.debounceTimeValue))
                .on('THEME.renderModals', _.debounce(_.bind(this.render, this), TT._.debounceTimeValue))
                .on('THEME.modalOpen', _.debounce(_.bind(this.render, this), TT._.debounceTimeValue))
                .on('SCLayoutCollections.productUnvalid', _.debounce(_.bind(this.render, this), TT._.debounceTimeValue))

        },

        onClickBtnPickup: function (evt) {
            this.filter.deliveryType = "pickup"
            this.filter.deliveryTypeString= "Emportée"
            $("body").find('.modal-window')
                .find('.js-mw-footer__commande-input').html("Emportée").end()
                .find('.js-mw-footer__commande-input').attr('delivery', 'Emportée').end()
                .find('.js-mw-footer__commande').addClass("chose")
            this.display_Window_2();
        },
        onClickBtnDelivery: function (evt) {
            this.filter.deliveryType = "delivery"
            this.filter.deliveryTypeString= "Livrée"
            $("body").find('.modal-window')
                .find('.js-mw-footer__commande-input').html("Livrée").end()
                .find('.js-mw-footer__commande-input').attr('delivery', 'Livrée').end()
                .find('.js-mw-footer__commande').addClass("chose")
            this.display_Window_2();
        },
        onChangeDatepicker: function (evt) {
            this.filter.date  = $(evt.currentTarget).val();

            $("body").find('.js-modal-window').find('.js-mw-footer__date-input').html(this.filter.date)
            $("body").find('.js-modal-window').find('.js-mw-footer__date').addClass("chose")

            this.display_Window_3()
        },
        onClickHour: function (evt) {
            this.filter.hour = $(evt.currentTarget).attr('data-name')
            var hourString = $(evt.currentTarget).html()
            $(".mw-3__item").removeClass('active')
            $(".mw-3__item[data-name='"+ this.filter.hour+"']").addClass('active')

            $("body").find('.js-modal-window')
                .find('.js-mw-footer__hour-input').html(hourString).end()
                .find('.js-mw-footer__hour').addClass("chose").end()
                .find('.js-mw-footer-btn1').addClass("show").end()
                .find('.js-mw-footer__title').removeClass("show")

        },
        onSubmit: function () {
            this.filter.submit =true
            this.emit("changedDataFilter",this.filter)
        },
        onCLickRollbackStep1:function(evt){
            this.display_Window_1();
            this.init_Window_2();
            this.init_Window_3();
        },
        onCLickRollbackStep2:function(evt){
            $("body").find('.js-modal-window').find('.js-mw-footer__hour').removeClass("show")
            this.display_Window_2()
        },
        onCLickRollbackStep3:function(evt){
            this.display_Window_3()
        },

        initFilterWithCart:function(){
            console.log("RUN initFilterWithCart")
            this.filter = {}
            this.filter.deliveryType = TT.cart.attributes._deliveryType || undefined
            this.filter.deliveryTypeString = TT.cart.attributes._deliveryTypeString || undefined
            this.filter.date = TT.cart.attributes.Date || undefined
            this.filter.hour = TT.cart.attributes.Heure || undefined
            if(!!TT.validateFilterCartAttributes()){
                this.display_Window_4()
            }else{
                this.display_Window_1()
            }
        },

        initDayDispo:function(){
            var days = {'Dimanche':0, 'Lundi':1, 'Mardi':2, 'Mercredi':3, 'Jeudi':4, 'Vendredi':5, 'Samedi':6}
            this.disponibility = Object.values(chefsJS)[0].disponibility
            //console.log({disponibility:this.disponibility})
            if(!this.filter.deliveryType){
                return false
            }
            this.dispoDay=   Object.keys(this.disponibility[this.filter.deliveryType]).map((el,index)=>{
                if(this.disponibility[this.filter.deliveryType][el].length>0)
                    return days[el]
                // return { [el] : this.disponibility[this.filter.deliveryType][el]}
            }).filter((el)=>!!el)
        },
        disableHours:function(){
            var days = ['Dimanche', 'Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi']
            var daySearch =days[ _TOOLS.strToDate(this.filter.date).getDay()];

            if(!this.disponibility[this.filter.deliveryType] ){
                return {error:"Aucun type de livraison choisi",code:"not delivery Type"};
            }
            if( !this.disponibility[this.filter.deliveryType][daySearch]){
                return {error:"le chefs n'est pas disponible le "+daySearch+" donc pas d horaire",code:"not hours"};
            }
            this.hoursCurrent = this.disponibility[this.filter.deliveryType][daySearch]
            for(Hourcurrent in  this.hoursCurrent){
                //si le jour J verifier chaque horaire pour les afficher ou pas
                if(_TOOLS.dayDiff(_TOOLS.dateToStr(this.nowDate),this.filter.date) === 0){
                    console.log("check hours pour le jour J " +this.ecartHour)

                    if(this.hoursCurrent[Hourcurrent] >= (this.nowDate.getHours()+this.ecartHour) ){
                        if(this.filter.deliveryType === "pickup"){
                            $('.js-mw-3__item[data-name="'+this.hoursCurrent[Hourcurrent]+':00"]').removeAttr("disabled")
                        }else{
                            $('.js-mw-3__item[data-name="'+(parseInt(this.hoursCurrent[Hourcurrent])-1)+':00-'+(parseInt(this.hoursCurrent[Hourcurrent])+1)+':00"]').removeAttr("disabled")
                        }
                    }
                }else{
                    if(this.filter.deliveryType === "pickup"){
                        $('.js-mw-3__item[data-name="'+this.hoursCurrent[Hourcurrent]+':00"]').removeAttr("disabled")
                    }else{
                        $('.js-mw-3__item[data-name="'+(parseInt(this.hoursCurrent[Hourcurrent])-1)+':00-'+(parseInt(this.hoursCurrent[Hourcurrent])+1)+':00"]').removeAttr("disabled")
                    }
                }

            }
        },

        DisableSpecificDates:function(date){
            /* Based upon Ankit function */

            var day = date.getDay()
            var m = date.getMonth();
            var d = date.getDate();
            var y = date.getFullYear();


            //enlever les date de fermeture
            var currentDate = (d<=9?"0":"") +d + '/'+ (m + 1<=9?"0":"") + (m + 1) + '/' + y ;

            if(this.disabledDates.length > 0){
                if(_TOOLS.isIntervalDate(currentDate,this.disabledDates.join(','))){
                    return [false];
                }
            }

            //refuser le weekend
            if(!this.isWeekends && [6,0].includes(parseInt(day))){
                return [false];
            }
            //afficher que les jours accepter du chef
            return [this.dispoDay.includes(parseInt(day))];

        },
        disableDaysDatepicker:function(date){
            // console.log({dispoDay:this.dispoDay,t:parseInt(date.getDay())})
            return [this.dispoDay.includes(parseInt(date.getDay()))]
        },

        init_Window_2: function() {
            this.initDayDispo()

            $("body").find('.js-modal-window').find('.js-datepicker').datepicker({
                altField: ".js-datepicker", closeText: 'Fermer', prevText: 'Précédent', nextText: 'Suivant',
                currentText: 'Aujourd\'hui',
                monthNames: ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'],
                monthNamesShort: ['Janv.', 'Févr.', 'Mars', 'Avril', 'Mai', 'Juin', 'Juil.', 'Août', 'Sept.', 'Oct.', 'Nov.', 'Déc.'],
                dayNames: ['Dimanche', 'Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi'],
                dayNamesShort: ['Dim.', 'Lun.', 'Mar.', 'Mer.', 'Jeu.', 'Ven.', 'Sam.'],
                dayNamesMin: ['Di', 'Lu', 'Ma', 'Me', 'Je', 'Ve', 'Sa'],
                weekHeader: 'Sem.',
                dateFormat: 'dd/mm/yy',
                firstDay: 1,
                minDate: 0,
                setDate: 0,
                showAnim: 'drop',
                beforeShowDay:_.bind(this.DisableSpecificDates,this),
                beforeShow: function( input, inst){
                    $(inst.dpDiv).addClass('modal-datepicker');
                }
            }).datepicker();

            $("body").find('.js-modal-window').find('.js-mw-footer__date-input').html("jj/mm/aaaa")
        },
        init_Window_3: function() {
            $("body").find('.js-modal-window')
                .find('.js-mw-footer__hour-input').html("hh:mm").end()
                .find('.js-mw-footer__hour').removeClass("chose").end()
                .find('.js-mw-footer-btn1').removeClass("show")
        },
        display_Window_1: function() {
            console.log("RUN display_Window_1")
            this.display_title_footer(1)
            this.display_window(1)
            $("body").find('.js-modal-window')
                .find('.js-mw-footer__commande-input').html("Emportée/Livrée").end()
                .find('.js-mw-footer__commande').removeClass("chose").end()

                .find('.js-mw-footer__date').removeClass("chose").end()
                .find('.js-mw-footer__date').removeClass("show").end()
                .find('.js-mw-footer__hour').removeClass("show").end()

                .find('.js-mw-footer-btn2').removeClass("show").end()
                .find('.mw-footer__block').removeClass("mw-flex").end()
                .find('.js-mw-footer__commande').addClass("show")


        },
        display_Window_2: function() {

            console.log("RUN display_Window_2")
            this.init_Window_2()
            this.init_Window_3()
            $("body").find('.js-modal-window')

                .find('.js-mw-footer-btn2').removeClass("show").end()
                .find('.js-mw-footer__date').addClass("show").end()
                .find('.js-mw-footer__date').removeClass("chose")

            this.display_title_footer(2)
            this.display_window(2)
        },
        display_Window_3: function() {

            console.log("RUN display_Window_3")
            this.init_Window_3()
            $("body").find('.js-modal-window')
                .find('.js-mw-footer-btn2').removeClass("show").end()
                .find('.js-mw-3').html(filtre_hours_template_modal).end()
                .find('.js-mw-footer__hour').addClass("show")

            $("body").find('.js-modal-window').find('.js-mw-3__item').attr("disabled","disabled")

            this.display_title_footer(3)
            this.display_window(3)

            if ( this.filter.deliveryType === 'delivery') {
                $("body").find('.js-modal-window')
                    .find('.js-mw-3__commande').removeClass("show").end()
                    .find('.js-mw-3__livraison').addClass("show")
            }else{
                $("body").find('.js-modal-window')
                    .find('.js-mw-3__livraison').removeClass("show").end()
                    .find('.js-mw-3__commande').addClass("show")
            }

            this.disableHours()

        },
        display_Window_4: function() {

            console.log("RUN display_Window_4")
            this.display_title_footer()
            this.display_window(4)

            $("body").find('.js-modal-window')
                .find('.js-mw-footer__hour').removeClass("show").end()
                .find('.js-mw-footer__date').removeClass("show").end()
                .find('.js-mw-footer__commande').removeClass("show").end()
                .find('.js-mw-footer-btn1').removeClass("show").end()
                .find('.js-mw-footer-btn2').addClass("show").end()
                .find('.mw-footer__block').addClass("mw-flex")
        },

        //gestion contenu des window en fonction step
        display_window:function(step){
            $("body").find(".js-modal-window")
                .find('.js-mw-1').removeClass("show").end()
                .find('.js-mw-2').removeClass("show").end()
                .find('.js-mw-3').removeClass("show").end()
                .find('.js-mw-4').removeClass("show")

            if(!!step){
                $("body").find(".js-modal-window")
                    .find('.js-mw-'+step).addClass("show")
            }
        },
        //gestion du title dans le footer
        display_title_footer:function(step){
            $("body").find(".mw__footer")
                .find('.js-title-1').removeClass("show").end()
                .find('.js-title-2').removeClass("show").end()
                .find('.js-title-3').removeClass("show")

            if(!!step){
                $("body").find(".mw__footer")
                    .find('.js-title-'+step).addClass("show")
            }
        }

    }

    //  SCFilterModal.prototype = _.merge(SCFilterMenu.prototype, _SCFilterModal);
    console.log("%cRENDER SC.filters_modal.js.liquid","background:yellow;color:#333")


}