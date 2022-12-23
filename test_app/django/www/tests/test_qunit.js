import QUnit from 'static@qunit';

QUnit.test('Dummy test', function(assert) {
  assert.expect(2);

  assert.true(true);
  assert.true(true);
});

QUnit.test('Dummy test 2', async function(assert) {
  assert.expect(1);
  const timeout = assert.async();
  setTimeout(() => {
    assert.true(true);
    timeout();
  }, 2000);
});
