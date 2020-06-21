<template>
  <geography-search-page
    :item-list="$store.state.cities"
    :select-item="selectCity"
    :select-subitem="selectGym"
    :item-title="itemTitle"
  />
</template>

<script>
import GeographySearchPage from "~/components/navigation/GeographySearchPage.vue"
import apiLibrary from "~/store/apiLibrary.js"
import _ from "lodash"

export default {
  components: {
    GeographySearchPage,
  },
  async fetch({ route, store }) {
    let url = `${process.env.BACKEND_URL}/affiliates/gyms/`
    const state = route.params["state"].replace(/-/gi, " ")
    if (state === store.state.constants.NOSTATE) {
      const country = route.params["country"].replace(/-/gi, " ")
      url += `?country=${country}`
    } else {
      url += `?state=${state}`
    }
    url = encodeURI(url)
    await apiLibrary.retrieveCities(url, store)
  },
  data() {
    return {
      itemTitle: "state",
      cityList: {},
      metaTags: [],
    }
  },
  computed: {
    fetchPageTitle: function () {
      return this.$store.state.constants.GEO_PAGE_TITLE.replace(
        "{}",
        _.capitalize(this.$route.params[this.itemTitle]).replace(/-/gi, " ")
      )
    },
    fetchNumberOfGymsInCountry: function () {
      const gymLists = Object.values(this.$store.state.cities)
      let numberOfGyms = 0
      gymLists.forEach((list) => {
        numberOfGyms += list.length
      })
      return numberOfGyms
    },
    fetchPageDescription: function () {
      const numberOfCities = Object.keys(this.$store.state.cities).length
      let locationName = ""
      if (this.itemTitle === "state") {
        locationName = "states"
      } else {
        locationName = "cities"
      }
      return `${this.fetchNumberOfGymsInCountry} gyms across ${numberOfCities} ${locationName}. Find the best CrossFit Gym in your City. Photos, Pricing, Contact Information and All You Need To Know Before Visiting`
    },
  },
  mounted() {
    this.getItemTitle()
    this.$retrievePathVariables(this.$store, this.$route.params)
    this.$generateBreadcrumb(this.$store, this.$route.params, this.itemTitle)
    this.metaTags = this.$generateMetaTags(
      this.$store,
      this.fetchPageTitle,
      this.fetchPageDescription,
      this.$store.state.constants.DEFAULT_GYM_THUMBNAIL
    )
  },
  methods: {
    getItemTitle() {
      if (
        this.$store.state[`current_state`] ===
        this.$store.state.constants.NOSTATE
      ) {
        this.itemTitle = "country"
      }
    },
    fetchGym(cityName, gymName) {
      const url = `${process.env.BACKEND_URL}/affiliates/?city__iexact=${cityName}&name__iexact=${gymName}`
      apiLibrary.retrieveGym(url, this.$store).then(() => {
        this.navigateToGym(cityName, gymName)
      })
    },
    navigateToGym(cityName, gymName) {
      this.$pushCleanedRoute(this.$router, `${cityName}/${gymName}/`)
    },
    selectCity(cityName) {
      this.$store.commit("SET_CURRENT_CITY", cityName)
      this.$pushCleanedRoute(this.$router, `${cityName}/`)
    },
    selectGym(gymName) {
      const cityName = this.$findParent(this.$store.state.cities, gymName)
      this.$store.commit("SET_CURRENT_CITY", cityName)
      this.fetchGym(cityName, gymName)
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
