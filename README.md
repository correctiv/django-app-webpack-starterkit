# django-app-webpack-starterkit

Develop django apps with a webpack-powered frontend build.

It supports **sass**, **es6**, and the builds get **hashes** into their filenames for better cache handling in production.

The frontend build is fully independent from the django stuff, so you can tweak / setup webpack to your own needs.

The webpack stuff is based on [this great starterkit](https://github.com/wbkd/yet-another-webpack-es6-starterkit) by [@wbkd](https://github.com/wbkd).

## how does it work

Basically, there is a templatetag that renders static urls to the `js`- and `css`-bundle, based on current circumstances:
- if used in production, just reference to the builds in `./static/`
- for developement, reference the `webpack-dev-server`-endpoint, like `http://localhost:1337`, including hot-replacement stuff.

The templatetag uses the information from [`webpack-bundle-tracker`](https://github.com/owais/webpack-bundle-tracker).

See `webpack_loader.py` for details.

## usage

rename this app, template folder and `./templatetags/my_app.py` to the name of your new app.

add your app to django's `settings.INSTALLED_APP`

render your bundle-urls with `{% webpack_bundle "js" %}` and `{% webpack_bundle "css" %}`, see `./templates/my_app/base.html` for example.

install webpack stuff via `npm install`

start webpack dev server via `npm run dev`

start django runserver (it defaults to port 8000. if your django dev server is running somewhere else, you need to adjust the `webpackConfig.devServer.headers`-setting for `Access-Control-Allow-Origin` in `./webpack.config-helper.js`)

### issues

sometimes it's helpful to remove the `./webpack-stats.json`-file and restart both dev servers.

## build for production

`npm run build`

this command will flush `./static/` first to avoid disk consumption because the bundles are hashed (and therefore for each build a new file is created)
