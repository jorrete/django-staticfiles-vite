import Qunit from 'qunit';

QUnit.done((event) => {
  window.qunitPassed = event.failed === 0;
});

export default Qunit;
