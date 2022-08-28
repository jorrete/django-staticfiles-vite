import styles from '/static/www/App.module.scss';
import './font.scss';

const App = () => {
  return (
    <div
      class={styles.App}
      onClick={() => console.log('click')}
    >
      preact!!!!!!
    </div>
  );
}

export default App;
