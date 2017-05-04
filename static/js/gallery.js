$(document).ready(function() {
	$("a.newword").each( function() {
		$(this).css({color: "hsla("+getRandomInt(0,360)+","+getRandomInt(50,100)+"%,"+getRandomInt(40, 70)+"%,1)" });
	});
	setTimeout( function() { document.location.reload(true); }, 5000 );
});