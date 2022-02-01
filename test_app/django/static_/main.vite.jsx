// import '@vite/client';
import mod from './module';
import www from 'www/mongo';
// import '../out';
import { render } from 'preact'
import App from './App.jsx';
// import color from 'color-convert';
import 'index.scss';
// console.log('main.jsx!!', mod, www, color);
console.log('main', mod, www);

render(<App />, document.getElementById('app'))
