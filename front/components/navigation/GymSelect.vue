<template>
  <gym-search-page
    :gym-list="$store.state.gyms"
    :select-item="selectGym"
    :item-title="itemTitle"
  />
</template>

<script>
import GymSearchPage from "~/components/navigation/GymSearchPage.vue"
import apiLibrary from "~/store/apiLibrary.js"
import _ from "lodash"
import reusableFunctionsLibrary from "~/store/reusableFunctionsLibrary.js"

export default {
  name: "GymSelect",
  components: {
    GymSearchPage,
  },
  async asyncData({ route, store }) {
    const country = route.params["country"].replace(/-/gi, " ")
    const state = route.params["state"].replace(/-/gi, " ")
    const city = route.params["city"].replace(/-/gi, " ")
    let url = `${process.env.BACKEND_URL}/gyms/?city__iexact=${city}&country__iexact=${country}`
    if (
      store.state.constants.COUNTRIES_WITH_STATES.indexOf(
        route.params["country"]
      ) === -1
    )
      url += `&full_state__iexact=${state}`

    await apiLibrary.retrieveGyms(url, store)

    let cityName = _.capitalize(route.params["city"]).replace(/-/gi, " ")
    let pageTitle = store.state.constants.GEO_PAGE_TITLE.replace("{}", cityName)
    let pageDescription = `The ${store.state.gyms.length} Best CrossFit Gym${
      store.state.gyms.length > 1 ? "s" : ""
    } in ${cityName}. Check Out The Latest Reviews, Pricing, Contact Information for CrossFit Gyms in ${cityName}`

    let metaTags = reusableFunctionsLibrary.generateMetaTags(
      store,
      pageTitle,
      pageDescription,
      store.state.constants.DEFAULT_GYM_THUMBNAIL,
      route.fullPath
    )

    return {
      metaTags: metaTags,
      pageTitle: pageTitle,
    }
  },
  data() {
    return {
      itemTitle: "city",
      metaTags: [],
      pageTitle: "",
    }
  },
  methods: {
    selectGym(selectedGym) {
      this.$store.commit("SET_GYM_OBJECT", selectedGym)
    },
  },
  head() {
    return {
      title: this.pageTitle,
      meta: this.metaTags,
    }
  },
}
</script>
