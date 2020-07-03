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
  name: "CityAndGymSelect",
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
    this.getItemTitle()
  },
  methods: {
    getItemTitle() {
      if (
        this.$store.state.constants.COUNTRIES_WITH_STATES.indexOf(
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
}
</script>
