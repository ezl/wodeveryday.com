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

export default {
  name: "GymSelect",
  components: {
    GymSearchPage,
  },
  async fetch({ route, store }) {
    const country = route.params["country"].replace(/-/gi, " ")
    const state = route.params["state"].replace(/-/gi, " ")
    const city = route.params["city"].replace(/-/gi, " ")
    let url = `${process.env.BACKEND_URL}/affiliates/?city__iexact=${city}&country__iexact=${country}`
    if (
      ["united-states", "australia", "canada"].indexOf(
        route.params["country"]
      ) === -1
    )
      url += `&full_state__iexact=${state}`
    url = encodeURI(url)

    await apiLibrary.retrieveGyms(url, store)
  },
  data() {
    return {
      itemTitle: "city",
      metaTags: [],
    }
  },
  computed: {
    fetchCityName: function () {
      return _.capitalize(this.$route.params[this.itemTitle]).replace(
        /-/gi,
        " "
      )
    },
    fetchPageTitle: function () {
      return this.$store.state.constants.GEO_PAGE_TITLE.replace(
        "{}",
        this.fetchCityName
      )
    },
    fetchPageDescription: function () {
      return `The ${this.$store.state.gyms.length} Best CrossFit Gyms in ${this.fetchCityName}. Check Out The Latest Reviews, Pricing, Contact Information for CrossFit Gyms in ${this.fetchCityName}`
    },
  },
  mounted() {
    this.metaTags = this.$generateMetaTags(
      this.$store,
      this.fetchPageTitle,
      this.fetchPageDescription,
      this.$store.state.constants.DEFAULT_GYM_THUMBNAIL
    )
  },
  methods: {
    selectGym(selectedGym) {
      this.$store.commit("SET_GYM_OBJECT", selectedGym)
    },
  },
  head() {
    return {
      title: this.fetchPageTitle,
      meta: this.metaTags,
    }
  },
}
</script>
