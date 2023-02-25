import styles from 'static@www/App.module.scss';
import './font.scss';

function Button() {
  return (
    <div>xxx</div>
  );
}

const App = () => {
  return (
    <div
      className={styles.App}
      onClick={() => console.log('click')}
    >
      <img width="20" src="/static/www/pics/fox.jpg" alt="" />
      <img width="20" src="static@www/pics/fox.jpg" alt="" />
      <Button />
      preact!!!!!!
    </div>
  );
};

export default App;
