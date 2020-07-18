import colors from "vuetify/es5/util/colors"
import redirectSSL from "redirect-ssl"

require("dotenv").config()
// import routes from "./utils/getRoutes.js"

export default {
  mode: "universal",
  /*
   ** Headers of the page
   */
  head: {
    titleTemplate: "%s | WOD Every Day",
    meta: [
      { charset: "utf-8" },
      { name: "viewport", content: "width=device-width, initial-scale=1" },
    ],
    link: [{ rel: "icon", type: "image/x-icon", href: "/default_favicon.ico" }],
    script: [
      {
        src: `https://maps.googleapis.com/maps/api/js?key=${process.env.GCP_API_KEY}&libraries=places`,
      },
    ],
  },
  serverMiddleware: [
    redirectSSL.create({
      exclude: ["localhost"],
      enabled: process.env.NODE_ENV === "production",
    }),
  ],
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
  buildModules: [
    "@nuxt/typescript-build",
    "@nuxtjs/vuetify",
    "@nuxtjs/dotenv",
    "@nuxtjs/gtm",
  ],
  gtm: {
    id: process.env.GTM_ID,
    pageTracking: true,
  },
  /*
   ** generate sitemap
   */
  // sitemap: {
  //   routes() {
  //     return routes.getAppRoutes()
  //   },
  //   path: "/sitemap.xml",
  //   gzip: true,
  //   generate: false,
  // },
  /*
   ** Nuxt.js modules
   */
  modules: ["nuxt-leaflet", "@nuxtjs/axios", "@nuxtjs/sitemap"],
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
