const envelope = document.getElementById('envelope');
const letter   = document.getElementById('letter');
const content  = document.getElementById('letter-content');
const bgMusic  = document.getElementById('bgMusic');
const musicBtn = document.getElementById('musicBtn');

// Nạp nội dung trang 2
fetch('love.txt')
  .then(r => r.text())
  .then(t => content.innerText = t)
  .catch(() => content.innerText = 'Không thể tải thư 💌');

// Click phong bì → mở nắp → kéo thư (hiện TRANG 1) → sau 3s lật sang TRANG 2
envelope.addEventListener('click', () => {
  if (envelope.classList.contains('animating')) return;
  envelope.classList.add('animating');

  // Mở nắp
  envelope.classList.add('open');

  // Kéo thư lên (trang 1 đang hiển thị)
  setTimeout(() => {
    envelope.classList.add('pull');
  }, 3000);

  // Sau 3s kể từ lúc kéo thư → flip sang trang 2
  setTimeout(() => {
    letter.classList.add('flip');
    setTimeout(() => {
      content.style.visibility = 'visible';
      typeLines(content);
    }, 2000);
  }, 6000);

  createHearts();

  // Nhạc (tuỳ chọn)
  if (bgMusic && bgMusic.paused) {
    bgMusic.play().then(() => {
      if (musicBtn) musicBtn.innerText = '⏸ Tạm dừng';
    }).catch(()=>{});
  }
});

// Nút nhạc (tuỳ chọn)
if (musicBtn && bgMusic) {
  musicBtn.addEventListener('click', () => {
    if (bgMusic.paused) {
      bgMusic.play(); musicBtn.innerText = '⏸ Tạm dừng';
    } else {
      bgMusic.pause(); musicBtn.innerText = '🎵 Phát nhạc';
    }
  });
}

// Gõ chữ 
function typeLines(container){
  // Bắt mọi kiểu xuống dòng: CRLF/LF/CR/U+2028
  const raw   = (container.textContent || '');
  const lines = raw.split(/\r\n|\n|\r|\u2028/g);

  const BASE_DELAY = 250;  // ms giữa các dòng
  const SPEED      = 80;   // ms/ký tự
  const HOLD       = 120;  // ms giữ caret cuối dòng

  container.innerHTML = '';

  let chain = Promise.resolve();
  lines.forEach((lineText, idx) => {
    // 1 dòng: [typeText][caret]
    const line   = document.createElement('div');
    line.className = 'line';

    const textEl  = document.createElement('span');
    textEl.className = 'typeText';

    const caretEl = document.createElement('span');
    caretEl.className = 'caret';

    line.append(textEl, caretEl);
    container.appendChild(line);

    // gõ theo chuỗi (dòng sau chờ dòng trước)
    chain = chain
      .then(() => typeOneLine(textEl, caretEl, lineText, SPEED, container))
      .then(() => wait(HOLD))
      .then(() => wait(BASE_DELAY));
  });

  chain.then(() => { container.style.overflow = 'auto'; });
}

function typeOneLine(textEl, caretEl, text, speed, scrollContainer){
  return new Promise(resolve => {
    const chars = (text && text.length) ? [...text] : [' '];
    let i = 0;
    caretEl.style.animation = 'caretBlink 1s steps(1) infinite';

    const timer = setInterval(() => {
      textEl.textContent += chars[i++];
      // auto scroll theo khi gõ
      scrollContainer.scrollTop = scrollContainer.scrollHeight;

      if (i >= chars.length){
        clearInterval(timer);
        caretEl.style.animation = 'none';
        caretEl.style.borderLeftColor = 'transparent';
        resolve();
      }
    }, speed);
  });
}

function wait(ms){ return new Promise(r => setTimeout(r, ms)); }


// Hiệu ứng trái tim bay
function createHearts() {
    for (let i = 0; i < 20; i++) spawnHeart();
    setInterval(spawnHeart, 800);
}
function spawnHeart() {
    const heart = document.createElement('div');
    heart.classList.add('floating-heart');
    heart.style.left = Math.random() * window.innerWidth + 'px';
    heart.style.top = window.innerHeight + 'px';
    heart.innerText = '❤';
    heart.style.fontSize = (Math.random() * 20 + 10) + 'px';
    document.body.appendChild(heart);
    setTimeout(() => heart.remove(), 4000);
}