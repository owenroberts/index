var stop = false;
var $words = $('.newword');
var $wordsContainer = $('#words');
var $counter = $('#counter');
var len = $words.length;
var count = 0;

asyncLoop({
	length: len,
	functionToLoop : function(loop, i) {
		setTimeout(function() {
			$words[i].style.display = "inline";
			$wordsContainer.append($words[i]).append('<br>');
			count++;
			$counter.text( count + " / " + len )
			loop();
		}, 1);
	},
	callback : function() {
		console.log("done!");
	}
});

$('body').on("mouseover", ".newword", function(){
	$(this).css({color:"hsla("+getRandomInt(30,300, 200)+","+getRandomInt(60,90)+"%,"+getRandomInt(50, 80)+"%,1)"});
})
.on("mouseout", ".newword", function(){
	$(this).css({color:"black"});
});