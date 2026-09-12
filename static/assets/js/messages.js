
setTimeout(function () {
    document.querySelectorAll('.auto-dismiss').forEach(function(el){
        let alert = new bootstrap.Alert(el);
        alert.close();
    });
}, 5000);
