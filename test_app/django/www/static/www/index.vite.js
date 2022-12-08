// import static
import mongo from 'static@www/mongo/index.js';
console.log(mongo);
// import relative
import foo from './foo';
// check preact render
import { render } from 'preact'
import App from './App.jsx';
// check import from node
import color from 'color-convert';

import deepClone from 'deep-clone';

// inject styles
import './styles.css';
import styles from './styles2.css';
import './main';
import './raw.css';
import fox from 'static@www/pics/fox.txt?raw';
console.log(fox);

console.log(deepClone);
console.log(styles);

console.log(color, mongo, foo);
render(<App foo={3} />, document.getElementById('app'))
