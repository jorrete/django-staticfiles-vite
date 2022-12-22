// eslint-disable-next-line no-undef
module.exports = {
  'env': {
    'node': true,
    'browser': true,
    'es2021': true
  },
  'extends': [
    'eslint:recommended',
    'plugin:react/recommended',
  ],
  'overrides': [
  ],
  'parserOptions': {
    'ecmaVersion': 'latest',
    'sourceType': 'module'
  },
  'plugins': [
    'react'
  ],
  'rules': {
    'node/no-missing-import': 'off',
    'react/react-in-jsx-scope': 'off',
    'node/no-extraneous-import': 'off',
    'node/no-unsupported-features/es-syntax': 'off',
  }
};
