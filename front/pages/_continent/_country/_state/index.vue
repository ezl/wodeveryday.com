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
  data() {
    return {
      itemTitle: "state",
      cityList: {},
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
  head() {
    return {
      title: this.fetchPageTitle,
      meta: [
        {
          hid: "description",
          name: "description",
          content: this.fetchPageDescription,
        },
        {
          property: "og:title",
          content: this.fetchPageTitle,
        },
        {
          property: "og:description",
          content: this.fetchPageDescription,
        },
        {
          property: "og:image",
          content: this.$store.state.constants.DEFAULT_GYM_THUMBNAIL,
        },
      ],
    }
  },
}
</script>
