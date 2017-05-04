function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

var asyncLoop = function(o) {
    var i=-1;
    var loop = function() {
        if (stop) return;
        i++;
        if (i==o.length){o.callback(); return;}
        o.functionToLoop(loop, i);
    }
    loop();
};
