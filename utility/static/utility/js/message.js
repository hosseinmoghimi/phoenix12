function show_message(app,title,body,color,duration){
    app.message={
        title:title,
        body:body,
        show:true,
        color:color
    }
    app.waiting=false
    app.loading=false
    app.wait=false
    setTimeout(() => {
        app.message={
            // body:message,
            show:false,
            // color:color
        } 
    }, duration);
}