let brands_app_data = {
    brands: brands_for_brands_app,
    
}
let brands_app_methods = {
    filter:function(){
    brands_app.brands=brands_for_brands_app.filter(brand=>brand.name.toUpperCase().indexOf(brands_app.search_for.toUpperCase())>-1)
    },
}  
    
let brands_app = new Vue({
    el: "#brands-app",
    data: {
        brands: brands_for_brands_app,
        search_for: "",
    waiting: false,
    message: { show: false },
    },
    methods: brands_app_methods,
}) 