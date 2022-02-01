import styles from './App.module.scss';

const App = () => {
  return (
    <div
      class={styles.App}
      onClick={() => console.log('click')}
    >
      preact hola hola
    </div>
  );
}

export default App;
