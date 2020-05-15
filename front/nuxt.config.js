import colors from "vuetify/es5/util/colors"
require("dotenv").config()

export default {
  mode: "universal",
  /*
   ** Headers of the page
   */
  head: {
    titleTemplate: "%s - " + process.env.npm_package_name,
    title: process.env.npm_package_name || "",
    meta: [
      { charset: "utf-8" },
      { name: "viewport", content: "width=device-width, initial-scale=1" },
      {
        hid: "description",
        name: "description",
        content: process.env.npm_package_description || "",
      },
    ],
    link: [{ rel: "icon", type: "image/x-icon", href: "/favicon.ico" }],
    __dangerouslyDisableSanitizers: ["script"],
    script: [
      {
        src: `https://maps.googleapis.com/maps/api/js?key=${process.env.GCP_API_KEY}&libraries=places`,
      },
      {
        innerHTML: `(function (w, d, s, l, i) {
          w[l] = w[l] || []
          w[l].push({ "gtm.start": new Date().getTime(), event: "gtm.js" })
          var f = d.getElementsByTagName(s)[0],
            j = d.createElement(s),
            dl = l != "dataLayer" ? "&l=" + l : ""
          j.async = true
          j.src = "https://www.googletagmanager.com/gtm.js?id=" + i + dl
          f.parentNode.insertBefore(j, f)
        })(window, document, "script", "dataLayer", "${process.env.GTM_ID}")`,
      },
    ],
  },
  /*
   ** Customize the progress-bar color
   */
  loading: { color: "#fff" },
  /*
   ** Global CSS
   */
  css: [],
  /*
   ** Plugins to load before mounting the App
   */
  plugins: [],
  /*
   ** Nuxt.js dev-modules
   */
  buildModules: ["@nuxt/typescript-build", "@nuxtjs/vuetify", "@nuxtjs/dotenv"],
  /*
   ** Nuxt.js modules
   */
  modules: ["nuxt-leaflet", "@nuxtjs/axios"],
  /*
   ** vuetify module configuration
   ** https://github.com/nuxt-community/vuetify-module
   */
  vuetify: {
    theme: {
      dark: true,
      themes: {
        dark: {
          primary: colors.blue.darken2,
          accent: colors.grey.darken3,
          secondary: colors.amber.darken3,
          info: colors.teal.lighten1,
          warning: colors.amber.base,
          error: colors.deepOrange.accent4,
          success: colors.green.accent3,
        },
      },
    },
  },
  /*
   ** Build configuration
   */
  build: {
    /*
     ** You can extend webpack config here
     */
    extend(config, ctx) {
      // Run ESLint on save
      if (ctx.isDev && ctx.isClient) {
        config.module.rules.push({
          enforce: "pre",
          test: /\.(js|vue)$/,
          loader: "eslint-loader",
          exclude: /(node_modules)/,
        })
      }
    },
  },
}
