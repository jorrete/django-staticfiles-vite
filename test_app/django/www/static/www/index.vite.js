// import from directory
import mongo from 'www/mongo';
// import relative
import foo from './foo';
// check preact render
import { render } from 'preact'
import App from './App.jsx';
// check import from node
import color from 'color-convert';


// inject styles
import './styles.css';

console.log(color, mongo, foo);
render(<App />, document.getElementById('app'))
