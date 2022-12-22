/* eslint-disable */
import QUnit from 'qunit';

QUnit.done((result) => {
  window.qunitResult = result;
  if (window._qunitDone) {
    window._qunitDone(result);
  }
});

window.qunitDone = (callback) => {
  if (window.qunitResult) {
    callback(window.qunitResult);
    return;
  }

  window._qunitDone = callback;
};

export { QUnit as default };
