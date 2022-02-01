import styles from './App.module.scss';

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
