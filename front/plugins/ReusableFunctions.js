import Vue from "vue"

Vue.prototype.$pushCleanedRoute = ($router, route) => {
  const cleanedRoute = encodeURI(route.toLowerCase().replace(/ /gi, "-"))
  $router.push(cleanedRoute)
}
