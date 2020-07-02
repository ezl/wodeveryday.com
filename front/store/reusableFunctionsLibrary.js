export default {
  generateMetaTags(store, title, description, image) {
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
    ]
  },
}
