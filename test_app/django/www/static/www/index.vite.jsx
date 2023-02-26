// import './styles.css';
// import styles from './styles2.css?inline';
// console.log({ styles });
// import './main';
// import './raw.css';
// // import 'static@download/congo.js';
// // import mongo from 'static@www/mongo';
// // console.log({ mongo });
// import foo_static from 'static@www/foo.js';
// console.log({ foo_static });
// import foo_relative from './foo';
import deepClone from 'deep-clone';
import { render } from 'preact';
import App from './vite/App';

console.log('www', deepClone);

// document.addEventListener('click', async () => {
//   const fox = await import('static@www/pics/fox.txt?raw');
//   console.log({ fox });
// });

render(<App />, document.getElementById('app'));
