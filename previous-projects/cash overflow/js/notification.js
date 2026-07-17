	var notifCount=document.getElementById('notif-count');
	var notif=2;

	var size='';
	var fontSize='1em';

	if(notif == 0){
		notifCount.style.backgroundColor='#3A6DAC';
		size='20px';
	}
	else if (Math.floor(notif/10) == 0) {
		size='20px';
	}
	else if(Math.floor(notif/10) < 10){
		size='23px';
	}
	else{
		fontSize='0.9em';
		size='30px';
		notif='100<sup>+</sup>';
	}
	notifCount.innerHTML=notif;
	notifCount.style.fontSize=fontSize;
	notifCount.style.borderRadius=size;
	notifCount.style.lineHeight=size;
	notifCount.style.height=size;
	notifCount.style.width=size;