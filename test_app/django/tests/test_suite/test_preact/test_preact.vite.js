import { render } from 'preact';
import App from './App';

render(<App />, document.getElementById('content'));

QUnit.module('import', () => {
  QUnit.test('succesful js import', assert => {
    assert.ok(true);
  });

  QUnit.test('succesful css import', assert => {
    assert.equal(getComputedStyle(document.body).fontSize, '20px');
  });

  QUnit.test('succesful preact render', assert => {
    assert.equal(
      document.getElementById('content').textContent,
      'preact!!',
    );
  });

  QUnit.test('succesful preact module styles', assert => {
    assert.equal(
      getComputedStyle(
        document.getElementById('content').firstElementChild
      ).backgroundColor,
      'rgb(255, 155, 0)',
    );
  });
});
