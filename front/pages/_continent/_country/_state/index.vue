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

export default {
  components: {
    GeographySearchPage,
  },
  data() {
    return {
      itemTitle: "state",
      cityList: {},
    }
  },
  mounted() {
    this.$retrievePathVariables(this.$store, this.$route.params)
    this.fetchCities()
    this.$generateBreadcrumb(this.$store, this.$route.params, this.itemTitle)
  },
  methods: {
    fetchCitiesURL() {
      let url = `${process.env.BACKEND_URL}/affiliates/gyms/`
      const state = this.$store.state[`current_${this.itemTitle}`]
      if (state === this.$store.state.constants.NOSTATE) {
        this.itemTitle = "country"
        const country = this.$store.state[`current_${this.itemTitle}`]
        url += `?country=${country}`
      } else {
        url += `?state=${state}`
      }
      url = encodeURI(url)
      return url
    },
    fetchCities() {
      const url = this.fetchCitiesURL()
      apiLibrary.retrieveCities(url, this.$store)
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
}
</script>
