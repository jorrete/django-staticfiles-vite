QUnit.module('import', () => {
  QUnit.test('succesful js import', assert => {
    assert.ok(true);
  });

  QUnit.test('succesful css import', assert => {
    assert.equal(getComputedStyle(document.body).fontSize, '20px');
  });
});
