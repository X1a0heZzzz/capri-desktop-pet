'use strict';
(() => {
  const data = window.CAPRI;
  const select = document.getElementById('pet-select');
  const canvas = document.getElementById('pet-canvas');
  const context = canvas.getContext('2d');
  const states = document.getElementById('states');
  const play = document.getElementById('play');
  const reduce = document.getElementById('reduce-motion');
  const speed = document.getElementById('speed');
  const status = document.getElementById('status');
  const labels = ['发呆 / 休息','向右移动','向左移动','打个招呼','小幅跳动','累了 / 躺下','等待 / 托腮','工作中','观察 / 打趣'];
  const caption = ['让她安静地待一会儿。','往右边挪一点。','往左边挪一点。','你好呀。','一点点雀跃。','今天也辛苦了。','等你回来。','陪你把事情做完。','让我再看一眼。'];
  let pet, image, row = 0, col = 0, playing = true, accumulated = 0, previous = 0, request = 0;
  const motionQuery = matchMedia('(prefers-reduced-motion: reduce)');
  reduce.checked = motionQuery.matches;
  playing = !reduce.checked;
  function draw() {
    if (!image || !pet) return;
    context.clearRect(0,0,canvas.width,canvas.height);
    context.imageSmoothingEnabled = pet.id !== 'capri-pixel';
    context.drawImage(image,col*192,row*208,192,208,0,0,384,416);
    document.getElementById('frame-label').textContent = `${pet.states[row].state} / ${col+1} OF ${pet.states[row].frames}`;
  }
  function sync() {
    play.textContent = playing ? '暂停播放' : '继续播放';
    play.disabled = reduce.checked;
    status.textContent = reduce.checked ? '已减少动态效果；仍可选择状态查看首帧。' : (playing ? '按角色包记录的时序播放 · 图集完全来自本地' :'已暂停 · 可选择其他状态');
    [...states.children].forEach((button,index) => button.setAttribute('aria-pressed', String(index === row)));
    document.querySelector('.stage-caption').textContent = caption[row];
    if (pet) canvas.setAttribute('aria-label',`${pet.name}：${labels[row]}`);
  }
  labels.forEach((label,index) => {
    const button = document.createElement('button');
    button.type = 'button'; button.textContent = label; button.setAttribute('aria-pressed',String(index===0));
    button.addEventListener('click',()=>{row=index;col=0;accumulated=0;sync();draw();});
    states.append(button);
  });
  function loadPet() {
    const token = ++request;
    const choice = data.pets.find(p=>p.id===select.value);
    const candidate = new Image();
    status.textContent = '正在载入本地图集…';
    candidate.onload = () => {
      if (token !== request) return;
      pet=choice;image=candidate;col=0;accumulated=0;
      document.getElementById('pet-label').textContent=pet.name;
      document.getElementById('download').href=pet.sprite;
      canvas.setAttribute('aria-label',`${pet.name}：${labels[row]}`);
      sync();draw();
    };
    candidate.onerror = () => { if(token===request) status.textContent='图集载入失败，请确认已完整解压仓库，保留 pets 文件夹。'; };
    candidate.src=choice.sprite;
  }
  select.addEventListener('change',loadPet);
  play.addEventListener('click',()=>{playing=!playing;accumulated=0;sync();});
  reduce.addEventListener('change',()=>{playing=!reduce.checked;col=0;accumulated=0;sync();draw();});
  motionQuery.addEventListener('change',event=>{reduce.checked=event.matches;reduce.dispatchEvent(new Event('change'));});
  speed.addEventListener('input',()=>{document.getElementById('speed-value').textContent=`${Number(speed.value)}×`;});
  document.getElementById('background').addEventListener('click',event=>{
    const active=document.getElementById('stage').classList.toggle('checker');
    event.currentTarget.setAttribute('aria-pressed',String(active));
  });
  document.addEventListener('visibilitychange',()=>{previous=0;accumulated=0;});
  function tick(time) {
    if(previous && image && playing && !reduce.checked && !document.hidden){
      accumulated += Math.min(time-previous,250)*Number(speed.value);
      let changed=false;
      while(accumulated>=pet.states[row].durationsMs[col]){
        accumulated-=pet.states[row].durationsMs[col];col=(col+1)%pet.states[row].frames;changed=true;
      }
      if(changed)draw();
    }
    previous=time;requestAnimationFrame(tick);
  }
  data.stages.forEach((stage,index)=>{
    const figure=document.createElement('figure');
    const imageLink=document.createElement('a');imageLink.href=stage.preview;imageLink.className='image-link';
    const thumbnail=document.createElement('img');thumbnail.src=stage.preview;thumbnail.alt=stage.name;thumbnail.loading='lazy';
    imageLink.append(thumbnail);figure.append(imageLink);
    const info=document.createElement('figcaption');
    const serial=document.createElement('span');serial.className='record-number';serial.textContent=`STAGE ${String(index+1).padStart(2,'0')}`;
    const title=document.createElement('h3');title.textContent=stage.name;
    const detail=document.createElement('p');detail.textContent=stage.package?'完整角色包 · 9种动作状态':'设计原稿 · 保留制作阶段';
    info.append(serial,title,detail);
    if(stage.package){const link=document.createElement('a');link.href=`pets/${stage.package}/spritesheet.webp`;link.download='';link.textContent='下载图集 ↗';info.append(link);}
    figure.append(info);document.getElementById('gallery').append(figure);
  });
  sync();loadPet();requestAnimationFrame(tick);
})();
