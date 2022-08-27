// import from directory
import mongo from '/static/www/mongo';
// import relative
import foo from './foo';
// check preact render
import { render } from 'preact'
import App from './App.jsx';
// check import from node
import color from 'color-convert';


// inject styles
import './styles.css';
import styles from './styles2.css';

console.log(styles);

console.log(color, mongo, foo);
render(<App />, document.getElementById('app'))
