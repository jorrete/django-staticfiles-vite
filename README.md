# django-staticfiles-vite (POC)

This package explores the integration of [vitejs](https://vitejs.dev/) as static asset provider during development.
It serves (and process accordingly with vitejs configuration). It is able to use imports (js and css) with the django static path like you would use in a django template, allowing to split js and css assets with in third party apps.
When using collectstatic in deployment the assets are compiled with vitejs.

# Status
There is an issue opened in [vitejs](https://github.com/vitejs/vite/pull/4679) that prevents to pass extra paths to the postcss configuration. Until that issue is fixed we use a patched version.
 

# Use

## Install
```
make install
```

## Dev
```
make dev
```

## Test

Run test suite

```
make test
```

To test manually each test run

```
make dev
```

Then navigate to **http://localhost:8000/tests/**
