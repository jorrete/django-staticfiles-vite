import style from './App.module.css';

export default function App() {
  return (
    <div
      className={style.App}
    >
      <div>
        foo
      </div>
      <div>
        <img src="static@fox.png" alt="" />
      </div>
      <div>
        <a href="/qunit/">qunit</a>
      </div>
    </div>
  );
}
