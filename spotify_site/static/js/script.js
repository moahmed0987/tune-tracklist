function nav_bar_responsive() {
    var x = document.querySelector(".nav-list")
    if (x.className === "nav-list") {
        x.className += " responsive";
    } else {
        x.className = "nav-list";
    }
}