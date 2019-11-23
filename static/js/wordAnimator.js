var stop = false;
var $words = $('.new-word');
var words = document.getElementsByClassName('new-word');
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
		}, 2);
	},
	callback : function() {
		console.log("done!");
	}
});

$('body').on("mouseover", ".new-word", function(){
	$(this).css({color:"hsla("+getRandomInt(30,300, 200)+","+getRandomInt(60,90)+"%,"+getRandomInt(50, 80)+"%,1)"});
})
.on("mouseout", ".new-word", function(){
	$(this).css({color:"black"});
});