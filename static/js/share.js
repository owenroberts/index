const shareButton = document.getElementById('share-button');
const share = document.getElementById('share');
const download = document.getElementById('download');
const copyURL = document.getElementById('copy-url');

if (title) { if (title == 'pasted') shareButton.style.display = 'none'; }

shareButton.onclick = function() {
	if (share.style.display != 'flex') share.style.display = 'flex';
	else share.style.display = 'none';
};

twitter.onclick = function() {
	const url = location.href;
	const msg = typeof noun != 'undefined' ? `${prefix}${noun}` : title;
	window.open(`https://twitter.com/intent/tweet?text=${msg} ${url}`, "_blank");
};

copyURL.onclick = function() {
	const el = document.createElement('textarea');
	el.value = location.href;
	document.body.appendChild(el);
	el.select();
	document.execCommand('copy');
	document.body.removeChild(el);
};

download.onclick = function() {
	html2canvas(document.getElementById('gallery'), {
		scale: 2,
		x: -128,
		y: -128,
		width: 1024,
		height: 1024
	}).then(canvas => {
		const image = canvas.toDataURL("image/png");
		
		// for ios 
		// https://stackoverflow.com/a/57896728
		const img = new Image();
		img.crossOrigin = "Anonymous";
		img.id = 'downloadImage';
		img.src = image;
		document.body.appendChild(img);

		const a = document.createElement('a');
		a.href = downloadImage.src; // id ?
		console.log(typeof noun)
		a.download = typeof noun != 'undefined' ? `${prefix}${noun}` : title;
		a.click();
		document.body.removeChild(img);

		// this works for desktop
		// seems to work on ios, creates the image (style needs to be fixed)
		// possible to open instagram?

	});
};
