# django-staticfiles-vite (POC)

This package explores the integration of [vitejs](https://vitejs.dev/) as static asset provider during development.
It serves (and process accordingly with vitejs configuration) static assets.

It is able to use imports (JS and CSS) with the DJANGO static path like you would use in a django template, allowing to split JS and CSS assets with in third party apps.

When using **collectstatic** in deployment the assets are compiled with vitejs.

Also allow to integrate easily npm dependencies as javascript assets.

## Status
There is an issue opened in [vitejs](https://github.com/vitejs/vite/pull/4679) that prevents to pass extra paths to the postcss configuration. Until that issue is fixed we use a patched version.

# Use

Create a **package.json** and a **vite.config.js** files in your project ddirectory and install dependencies.

In you **settings.py** add **staticfiles_vite** before **staticfiles** app.
```python
INSTALLED_APPS = [
    ...
    "django_staticfiles_vite",
    "django.contrib.staticfiles",
    ...
]
```
## Commands

### runserver
Overrides default **runserver** and adds one that spawns a vitejs server automatically.
```bash
runserver --vite=auto
```

### collectstatic
Overrides default **collectstatic** and adds one that process the assets with vitejs
```bash
collectstatic --vite
```

# Development

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
