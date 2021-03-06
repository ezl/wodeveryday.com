export default {
  pushCleanedRoute(router, route) {
    const cleanedRoute = encodeURI(route.toLowerCase().replace(/ /gi, "-"))
    router.push(cleanedRoute)
  },
  generateMetaTags(store, title, description, image, urlPath) {
    return [
      {
        property: "og:type",
        content: "website",
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
      {
        property: "og:url",
        content: "https://www.wodeveryday.com" + urlPath,
      },
      {
        property: "og:image:width",
        content: 220,
      },
      {
        property: "og:image:height",
        content: 220,
      },
    ]
  },
}
