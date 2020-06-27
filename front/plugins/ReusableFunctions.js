import Vue from "vue"

Vue.prototype.$generateMetaTags = (store, title, description, image) => {
  let url = process.client ? window.location.href : ""
  return [
    {
      property: "og:type",
      content: "website",
    },
    {
      property: "og:url",
      content: url,
    },
    {
      property: "og:site_name",
      content: store.state.constants.WEBSITE_TITLE,
    },
    {
      name: "twitter:title",
      property: "og:title",
      content: title,
    },
    {
      name: "twitter:description",
      property: "og:description",
      content: description,
    },
    {
      property: "og:image",
      content: image,
    },
    {
      name: "twitter:image",
      content: image,
    },
  ]
}

Vue.prototype.$pushCleanedRoute = ($router, route) => {
  const cleanedRoute = encodeURI(route.toLowerCase().replace(/ /gi, "-"))
  $router.push(cleanedRoute)
}
