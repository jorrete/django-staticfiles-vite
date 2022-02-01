import styles from './App.module.scss';
import 'www/font.scss';

const App = () => {
  return (
    <div
      class={styles.App}
      onClick={() => console.log('click')}
    >
      preact!!
    </div>
  );
}

export default App;
