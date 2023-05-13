function nav_bar_responsive() {
    var x = document.querySelector(".nav-bar")
    if (x.className === "nav-bar") {
        x.className += " responsive";
    } else {
        x.className = "nav-bar";
    }
}