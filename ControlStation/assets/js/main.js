$(document).ready(function(){
    console.log("Control Station Online");
    
    $("#ds-robot-enable-btn").click(function(){
        $("#ds-robot-enable-btn").addClass("active-btn");
        $("#ds-robot-enable-btn").attr("disabled", true);
        $("#ds-robot-disable-btn").removeClass("active-btn");
        $("#ds-robot-disable-btn").attr("disabled", false);
    })
    
    $("#ds-robot-disable-btn").click(function(){
        $("#ds-robot-disable-btn").addClass("active-btn");
        $("#ds-robot-disable-btn").attr("disabled", true);
        $("#ds-robot-enable-btn").removeClass("active-btn");
        $("#ds-robot-enable-btn").attr("disabled", false);
    })
    
    //
    
    $("#ds-window-main-btn").click(function(){
        $("#window-main").removeClass("hidden");
        $("#window-USB").addClass("hidden");
        
        $("#ds-window-main-btn").addClass("btn-primary");
        $("#ds-window-main-btn").removeClass("btn-secondary");
        
        $("#ds-window-usb-btn").removeClass("btn-primary");
        $("#ds-window-usb-btn").addClass("btn-secondary");
  
    })
    
    $("#ds-window-usb-btn").click(function(){
        $("#window-main").addClass("hidden");
        $("#window-USB").removeClass("hidden");
        
        $("#ds-window-main-btn").removeClass("btn-primary");
        $("#ds-window-main-btn").addClass("btn-secondary");
        
        $("#ds-window-usb-btn").addClass("btn-primary");
        $("#ds-window-usb-btn").removeClass("btn-secondary");
    })
    
    var usbList = document.getElementById("usb-panel-scrollable");
    Sortable.create(usbList, {
        draggable: ".usb-panel-device-item",
        ghostClass: "usb-panel-device-item-ghost"
    });
    
})