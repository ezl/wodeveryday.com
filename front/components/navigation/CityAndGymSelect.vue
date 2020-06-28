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
  name: "CityAndGymSelect",
  components: {
    GeographySearchPage,
  },
  async fetch({ route, store }) {
    let url = `${process.env.BACKEND_URL}/gyms/gyms/`
    const state = route.params["state"].replace(/-/gi, " ")
    if (
      ["united-states", "australia", "canada"].indexOf(
        this.$route.params["country"]
      ) === -1
    ) {
      const country = route.params["country"].replace(/-/gi, " ")
      url += `?country=${country}`
    } else {
      url += `?state=${state}`
    }

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
        ["united-states", "australia", "canada"].indexOf(
          this.$route.params["country"]
        ) === -1
      ) {
        this.itemTitle = "country"
      }
    },
    fetchGym(cityName, gymNameSlug) {
      const url = `${process.env.BACKEND_URL}/gyms/?name_slug__iexact=${gymNameSlug}`
      apiLibrary.retrieveGym(url, this.$store).then(() => {
        this.navigateToGym(cityName, gymNameSlug)
      })
    },
    navigateToGym(cityName, gymNameSlug) {
      this.$router.replace({ path: `/gym/${gymNameSlug}` })
    },
    selectCity(cityName) {
      this.$pushCleanedRoute(this.$router, `${cityName}/`)
    },
    selectGym(cityName, gymNameSlug) {
      this.fetchGym(cityName, gymNameSlug)
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
