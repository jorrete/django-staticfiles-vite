import './styles.css';
import styles from './styles2.css';
console.log({ styles });
import './main';
import './raw.css';
import fox from 'static@www/pics/fox.txt?raw';
import 'static@download/congo.js';
import mongo from 'static@www/mongo';
console.log({ mongo });
import foo_static from 'static@www/foo.js';
console.log({ foo_static });
import foo_relative from './foo';
console.log({ foo_relative });
import { render } from 'preact'
import App from './App.jsx';
import color from 'color-convert';
console.log({ color });
import deepClone from 'deep-clone';
console.log({ deepClone });
console.log({ fox });

render(<App foo={3} />, document.getElementById('app'))
