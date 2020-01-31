const loading = document.getElementById('loading');
const refreshBtn = document.getElementById('refresh');

refreshBtn.onclick = function() {
	loading.style.display = 'block';
	location.reload();
};

