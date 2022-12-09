import './index.css';
console.log('vite download');

document.addEventListener('click', async () => {
  const fox = await import('static@www/pics/fox.txt?raw');
  console.log({ fox });
});
