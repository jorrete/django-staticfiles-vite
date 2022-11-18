import styles from '/static/www/App.module.scss';
import './font.scss';

function Button() {
  return (
    <div>xxx</div>
  )
}

const App = () => {
  return (
    <div
      class={styles.App}
      onClick={() => console.log('click')}
    >
      <Button />
      preact!!!!!!
    </div>
  );
}

export default App;
