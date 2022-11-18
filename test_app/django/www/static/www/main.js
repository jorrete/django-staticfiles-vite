// import from directory
import mongo from '/static/www/mongo';
// import relative
import foo from './foo';
// check preact render
import { render } from 'preact'
// check import from node
import color from 'color-convert';


// inject styles
import './styles.css';
import styles from './styles2.css';

console.log(styles);

console.log('main', color, mongo, foo);
